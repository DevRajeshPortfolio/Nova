# types.py
# Nova Programming Language - Type System

import json
import re
from datetime import datetime

class Type:
    """Base type class"""
    
    def __init__(self, name):
        self.name = name
    
    def validate(self, value):
        """Validate a value against this type"""
        raise NotImplementedError
    
    def __repr__(self):
        return f"Type({self.name})"


class StringType(Type):
    """String type"""
    
    def __init__(self, min_length=None, max_length=None, pattern=None):
        super().__init__('string')
        self.min_length = min_length
        self.max_length = max_length
        self.pattern = pattern
    
    def validate(self, value):
        if not isinstance(value, str):
            return False, f"Expected string, got {type(value).__name__}"
        
        if self.min_length and len(value) < self.min_length:
            return False, f"String too short (min {self.min_length})"
        
        if self.max_length and len(value) > self.max_length:
            return False, f"String too long (max {self.max_length})"
        
        if self.pattern and not re.match(self.pattern, value):
            return False, f"String doesn't match pattern {self.pattern}"
        
        return True, None


class NumberType(Type):
    """Number type"""
    
    def __init__(self, min_value=None, max_value=None, integer=False):
        super().__init__('number')
        self.min_value = min_value
        self.max_value = max_value
        self.integer = integer
    
    def validate(self, value):
        if self.integer:
            if not isinstance(value, int):
                return False, f"Expected integer, got {type(value).__name__}"
        else:
            if not isinstance(value, (int, float)):
                return False, f"Expected number, got {type(value).__name__}"
        
        if self.min_value is not None and value < self.min_value:
            return False, f"Value below minimum {self.min_value}"
        
        if self.max_value is not None and value > self.max_value:
            return False, f"Value above maximum {self.max_value}"
        
        return True, None


class BooleanType(Type):
    """Boolean type"""
    
    def __init__(self):
        super().__init__('boolean')
    
    def validate(self, value):
        if not isinstance(value, bool):
            return False, f"Expected boolean, got {type(value).__name__}"
        return True, None


class ListType(Type):
    """List type"""
    
    def __init__(self, item_type=None, min_length=0, max_length=None):
        super().__init__('list')
        self.item_type = item_type
        self.min_length = min_length
        self.max_length = max_length
    
    def validate(self, value):
        if not isinstance(value, list):
            return False, f"Expected list, got {type(value).__name__}"
        
        if len(value) < self.min_length:
            return False, f"List too short (min {self.min_length})"
        
        if self.max_length and len(value) > self.max_length:
            return False, f"List too long (max {self.max_length})"
        
        if self.item_type:
            for i, item in enumerate(value):
                valid, error = self.item_type.validate(item)
                if not valid:
                    return False, f"Item {i}: {error}"
        
        return True, None


class ObjectType(Type):
    """Object type"""
    
    def __init__(self, schema=None, required=None, additional=False):
        super().__init__('object')
        self.schema = schema or {}
        self.required = required or []
        self.additional = additional
    
    def validate(self, value):
        if not isinstance(value, dict):
            return False, f"Expected object, got {type(value).__name__}"
        
        # Check required fields
        for field in self.required:
            if field not in value:
                return False, f"Missing required field: {field}"
        
        # Validate fields
        for field, field_type in self.schema.items():
            if field in value:
                valid, error = field_type.validate(value[field])
                if not valid:
                    return False, f"Field '{field}': {error}"
        
        # Check additional fields
        if not self.additional:
            extra_fields = set(value.keys()) - set(self.schema.keys()) - set(self.required)
            if extra_fields:
                return False, f"Unexpected fields: {', '.join(extra_fields)}"
        
        return True, None


class EmailType(StringType):
    """Email type"""
    
    def __init__(self):
        super().__init__(
            min_length=3,
            max_length=255,
            pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        self.name = 'email'


class URLType(StringType):
    """URL type"""
    
    def __init__(self):
        super().__init__(
            pattern=r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$'
        )
        self.name = 'url'


class DateType(Type):
    """Date type"""
    
    def __init__(self, format='%Y-%m-%d'):
        super().__init__('date')
        self.format = format
    
    def validate(self, value):
        if isinstance(value, datetime):
            return True, None
        
        if not isinstance(value, str):
            return False, f"Expected date string, got {type(value).__name__}"
        
        try:
            datetime.strptime(value, self.format)
            return True, None
        except ValueError:
            return False, f"Invalid date format, expected {self.format}"


class TypeRegistry:
    """Type registry for managing types"""
    
    def __init__(self):
        self.types = {
            'string': StringType(),
            'number': NumberType(),
            'integer': NumberType(integer=True),
            'boolean': BooleanType(),
            'list': ListType(),
            'object': ObjectType(),
            'email': EmailType(),
            'url': URLType(),
            'date': DateType()
        }
    
    def register(self, name, type_obj):
        """Register a type"""
        self.types[name] = type_obj
    
    def get(self, name):
        """Get a type by name"""
        return self.types.get(name)
    
    def create_type_from_annotation(self, annotation):
        """Create type from annotation string"""
        if isinstance(annotation, Type):
            return annotation
        
        if not isinstance(annotation, str):
            return None
        
        # Parse simple types
        if annotation in self.types:
            return self.types[annotation]
        
        # Parse list types: list[string], list[number], etc.
        if annotation.startswith('list[') and annotation.endswith(']'):
            inner = annotation[5:-1]
            inner_type = self.create_type_from_annotation(inner)
            if inner_type:
                return ListType(inner_type)
        
        # Parse object types: object{name: string, age: number}
        if annotation.startswith('object{') and annotation.endswith('}'):
            schema_str = annotation[7:-1]
            schema = {}
            for field in schema_str.split(','):
                if ':' in field:
                    name, type_str = field.strip().split(':', 1)
                    type_obj = self.create_type_from_annotation(type_str.strip())
                    if type_obj:
                        schema[name.strip()] = type_obj
            return ObjectType(schema)
        
        return None


class TypeChecker:
    """Type checker for Nova code"""
    
    def __init__(self):
        self.registry = TypeRegistry()
        self.errors = []
        self.warnings = []
        self.variable_types = {}
        self.function_signatures = {}
    
    def check(self, ast):
        """Check types in AST"""
        self.errors = []
        self.warnings = []
        
        for node in ast:
            self._check_node(node)
        
        return self.errors, self.warnings
    
    def _check_node(self, node):
        """Check types in a node"""
        if node.node_type == 'Assignment':
            self._check_assignment(node)
        elif node.node_type == 'NumberInput':
            self.variable_types[node.name] = NumberType()
        elif node.node_type == 'Input':
            self.variable_types[node.name] = StringType()
        elif node.node_type == 'Checkbox':
            self.variable_types[node.name] = BooleanType()
        elif node.node_type == 'Dropdown':
            self.variable_types[node.name] = StringType()
        elif node.node_type == 'Action':
            self._check_function(node)
        elif hasattr(node, 'children'):
            for child in node.children:
                self._check_node(child)
    
    def _check_assignment(self, node):
        """Check assignment types"""
        var_name = node.variable
        value = node.value
        
        # Infer value type
        value_type = self._infer_type(value)
        
        if var_name in self.variable_types:
            expected_type = self.variable_types[var_name]
            valid, error = expected_type.validate(value_type)
            if not valid:
                self.errors.append(f"Type mismatch for '{var_name}': {error}")
        else:
            self.variable_types[var_name] = value_type
    
    def _check_function(self, node):
        """Check function types"""
        if hasattr(node, 'params'):
            self.function_signatures[node.name] = {
                'params': node.params,
                'return_type': getattr(node, 'return_type', None)
            }
    
    def _infer_type(self, value):
        """Infer the type of a value"""
        if value is None:
            return None
        
        if hasattr(value, 'value'):
            value = value.value
        
        if isinstance(value, str):
            return StringType()
        elif isinstance(value, (int, float)):
            return NumberType()
        elif isinstance(value, bool):
            return BooleanType()
        elif isinstance(value, list):
            if value:
                item_types = [self._infer_type(v) for v in value]
                # Use first non-None type
                for t in item_types:
                    if t:
                        return ListType(t)
            return ListType()
        elif isinstance(value, dict):
            schema = {k: self._infer_type(v) for k, v in value.items() if v is not None}
            return ObjectType(schema)
        elif hasattr(value, 'node_type'):
            # AST node
            if value.node_type == 'String':
                return StringType()
            elif value.node_type == 'Number':
                return NumberType()
            elif value.node_type == 'Boolean':
                return BooleanType()
        
        return None


def annotate_type(value, type_annotation):
    """Annotate a value with a type"""
    registry = TypeRegistry()
    type_obj = registry.create_type_from_annotation(type_annotation)
    
    if type_obj:
        valid, error = type_obj.validate(value)
        if not valid:
            raise TypeError(f"Type annotation error: {error}")
    
    return value