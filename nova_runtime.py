# nova_runtime.py
# Nova Programming Language - Browser Runtime

import json
import os

class NovaRuntime:
    def __init__(self):
        self.variables = {}
        self.components = {}
        self.event_handlers = {}
        self.dom_references = {}
        self.state = {}
        self.list_store = {}
        self.runtime_ast = None
        
    def compile_for_browser(self, source_path, output_path):
        """Compile Nova source to browser-ready format"""
        from lexer import Lexer
        from parser import Parser
        from nodes import ValueNode, BinaryOpNode
        
        # Parse the source
        with open(source_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        lexer = Lexer(source_path, source)
        tokens, error = lexer.make_tokens()
        
        if error:
            print(f"Error: {error.as_string()}")
            return False
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Generate runtime JSON
        runtime_code = self._generate_runtime_json(ast)
        
        # Write runtime HTML
        self._generate_browser_bundle(runtime_code, output_path)
        
        return True
    
    def _generate_runtime_json(self, ast):
        """Convert AST to JSON for browser runtime"""
        runtime = {
            'variables': {},
            'components': {},
            'elements': [],
            'events': [],
            'logic': []
        }
        
        for node in ast:
            self._process_node_for_runtime(node, runtime)
        
        return json.dumps(runtime, indent=2)
    
    def _process_node_for_runtime(self, node, runtime):
        """Process a node for runtime JSON"""
        if node.node_type == 'NumberInput':
            runtime['variables'][node.name] = node.value
            runtime['elements'].append({
                'type': 'number_input',
                'id': node.name,
                'value': node.value
            })
        elif node.node_type == 'Button':
            runtime['elements'].append({
                'type': 'button',
                'id': node.name,
                'text': node.text
            })
        elif node.node_type == 'When':
            runtime['events'].append({
                'element': node.element,
                'event': node.event,
                'actions': self._process_actions(node.actions)
            })
        elif node.node_type == 'Assignment':
            runtime['variables'][node.variable] = self._get_value(node.value)
        elif node.node_type == 'If':
            runtime['logic'].append({
                'type': 'if',
                'condition': self._get_condition(node.condition),
                'body': self._process_actions(node.body)
            })
        elif hasattr(node, 'children'):
            for child in node.children:
                self._process_node_for_runtime(child, runtime)
    
    def _get_value(self, value_node):
        """Extract value from a node"""
        if hasattr(value_node, 'value'):
            return value_node.value
        return value_node
    
    def _get_condition(self, condition):
        """Extract condition as string"""
        if hasattr(condition, 'left') and hasattr(condition, 'right'):
            left = self._get_value(condition.left)
            right = self._get_value(condition.right)
            return f"{left} {condition.operator} {right}"
        return str(condition)
    
    def _process_actions(self, actions):
        """Process a list of actions"""
        result = []
        for action in actions:
            if action.node_type == 'Popup':
                result.append({'type': 'popup', 'message': action.message})
            elif action.node_type == 'Assignment':
                result.append({
                    'type': 'assign',
                    'variable': action.variable,
                    'value': self._get_value(action.value)
                })
            elif action.node_type == 'Show':
                result.append({'type': 'show', 'element': action.element})
            elif action.node_type == 'Hide':
                result.append({'type': 'hide', 'element': action.element})
            elif action.node_type == 'Enable':
                result.append({'type': 'enable', 'element': action.element})
            elif action.node_type == 'Disable':
                result.append({'type': 'disable', 'element': action.element})
        return result
    
    def _generate_browser_bundle(self, runtime_json, output_path):
        """Generate complete HTML bundle with runtime"""
        html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nova Runtime App</title>
    <link rel="stylesheet" href="style.css">
    <style>
        /* Nova Runtime Styles */
        .nova-container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .nova-button {{ background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }}
        .nova-button:hover {{ background: #0056b3; }}
        .nova-input {{ padding: 8px 12px; border: 1px solid #ddd; border-radius: 4px; width: 100%; max-width: 300px; }}
        .nova-label {{ display: block; margin: 5px 0; font-weight: 500; }}
        .nova-input-group {{ margin: 10px 0; }}
        .nova-heading {{ margin: 20px 0 10px; font-size: 2.5em; }}
        .nova-text {{ margin: 10px 0; }}
        .nova-hidden {{ display: none !important; }}
        .nova-disabled {{ opacity: 0.5; pointer-events: none; }}
    </style>
</head>
<body>
    <div id="app" class="nova-container"></div>
    
    <script>
        // Nova Runtime Engine
        class NovaRuntime {{
            constructor() {{
                this.variables = {{}};
                this.elements = {{}};
                this.eventHandlers = [];
                this.app = document.getElementById('app');
            }}
            
            loadRuntime(runtimeData) {{
                this.data = runtimeData;
                this.variables = runtimeData.variables || {{}};
                
                // Build UI
                this.buildUI(runtimeData.elements || []);
                
                // Setup events
                this.setupEvents(runtimeData.events || []);
                
                // Execute logic
                this.executeLogic(runtimeData.logic || []);
            }}
            
            buildUI(elements) {{
                for (let el of elements) {{
                    const element = this.createElement(el);
                    if (el.id) {{
                        this.elements[el.id] = element;
                    }}
                }}
            }}
            
            createElement(el) {{
                let element;
                switch(el.type) {{
                    case 'button':
                        element = document.createElement('button');
                        element.className = 'nova-button';
                        element.id = el.id;
                        element.textContent = el.text || el.id;
                        this.app.appendChild(element);
                        break;
                    case 'number_input':
                        const container = document.createElement('div');
                        container.className = 'nova-input-group';
                        const label = document.createElement('label');
                        label.className = 'nova-label';
                        label.textContent = el.id;
                        label.htmlFor = el.id;
                        container.appendChild(label);
                        element = document.createElement('input');
                        element.type = 'number';
                        element.className = 'nova-input';
                        element.id = el.id;
                        element.value = el.value || 0;
                        container.appendChild(element);
                        this.app.appendChild(container);
                        break;
                    case 'text':
                        element = document.createElement('p');
                        element.className = 'nova-text';
                        element.textContent = el.content || '';
                        this.app.appendChild(element);
                        break;
                    case 'heading':
                        element = document.createElement('h1');
                        element.className = 'nova-heading';
                        element.textContent = el.content || '';
                        this.app.appendChild(element);
                        break;
                    case 'input':
                        const inputContainer = document.createElement('div');
                        inputContainer.className = 'nova-input-group';
                        const inputLabel = document.createElement('label');
                        inputLabel.className = 'nova-label';
                        inputLabel.textContent = el.name;
                        inputLabel.htmlFor = el.name;
                        inputContainer.appendChild(inputLabel);
                        element = document.createElement('input');
                        element.type = 'text';
                        element.className = 'nova-input';
                        element.id = el.name;
                        element.placeholder = el.placeholder || '';
                        inputContainer.appendChild(element);
                        this.app.appendChild(inputContainer);
                        break;
                    case 'checkbox':
                        const cbContainer = document.createElement('div');
                        cbContainer.className = 'nova-checkbox-group';
                        element = document.createElement('input');
                        element.type = 'checkbox';
                        element.id = el.name;
                        if (el.checked) element.checked = true;
                        cbContainer.appendChild(element);
                        const cbLabel = document.createElement('label');
                        cbLabel.className = 'nova-label';
                        cbLabel.textContent = el.label || el.name;
                        cbLabel.htmlFor = el.name;
                        cbContainer.appendChild(cbLabel);
                        this.app.appendChild(cbContainer);
                        break;
                    case 'dropdown':
                        const ddContainer = document.createElement('div');
                        ddContainer.className = 'nova-input-group';
                        const ddLabel = document.createElement('label');
                        ddLabel.className = 'nova-label';
                        ddLabel.textContent = el.name;
                        ddLabel.htmlFor = el.name;
                        ddContainer.appendChild(ddLabel);
                        element = document.createElement('select');
                        element.className = 'nova-dropdown';
                        element.id = el.name;
                        for (let option of (el.options || [])) {{
                            const opt = document.createElement('option');
                            opt.value = option;
                            opt.textContent = option;
                            if (option === el.selected) opt.selected = true;
                            element.appendChild(opt);
                        }}
                        ddContainer.appendChild(element);
                        this.app.appendChild(ddContainer);
                        break;
                    default:
                        console.warn('Unknown element type:', el.type);
                }}
                return element;
            }}
            
            setupEvents(events) {{
                for (let evt of events) {{
                    const element = evt.element === 'document' 
                        ? document 
                        : document.getElementById(evt.element);
                    if (element) {{
                        const eventName = this.getEventName(evt.event);
                        element.addEventListener(eventName, (e) => {{
                            this.executeActions(evt.actions, e);
                        }});
                    }}
                }}
            }}
            
            getEventName(eventType) {{
                const map = {{
                    'clicked': 'click',
                    'doubleclicked': 'dblclick',
                    'rightclicked': 'contextmenu',
                    'hovered': 'mouseenter',
                    'hoverends': 'mouseleave',
                    'mousemoves': 'mousemove',
                    'mousewheel': 'wheel',
                    'keypressed': 'keydown',
                    'keyreleased': 'keyup',
                    'enterpressed': 'keydown',
                    'escapepressed': 'keydown',
                    'spacepressed': 'keydown',
                    'inputchanged': 'input',
                    'submitted': 'submit',
                    'focused': 'focus',
                    'blur': 'blur',
                    'DOMContentLoaded': 'DOMContentLoaded',
                    'beforeunload': 'beforeunload',
                    'scroll': 'scroll'
                }};
                return map[eventType] || eventType;
            }}
            
            executeActions(actions, event) {{
                for (let action of actions) {{
                    this.executeAction(action, event);
                }}
                // Re-render reactive elements
                this.updateReactiveUI();
            }}
            
            executeAction(action, event) {{
                switch(action.type) {{
                    case 'popup':
                        alert(action.message);
                        break;
                    case 'assign':
                        this.variables[action.variable] = action.value;
                        break;
                    case 'show':
                        const showEl = document.getElementById(action.element);
                        if (showEl) showEl.classList.remove('nova-hidden');
                        break;
                    case 'hide':
                        const hideEl = document.getElementById(action.element);
                        if (hideEl) hideEl.classList.add('nova-hidden');
                        break;
                    case 'enable':
                        const enableEl = document.getElementById(action.element);
                        if (enableEl) enableEl.classList.remove('nova-disabled');
                        break;
                    case 'disable':
                        const disableEl = document.getElementById(action.element);
                        if (disableEl) disableEl.classList.add('nova-disabled');
                        break;
                    default:
                        console.warn('Unknown action type:', action.type);
                }}
            }}
            
            executeLogic(logic) {{
                for (let item of logic) {{
                    if (item.type === 'if') {{
                        try {{
                            const condition = this.evaluateCondition(item.condition);
                            if (condition) {{
                                this.executeActions(item.body);
                            }}
                        }} catch(e) {{
                            console.warn('Condition evaluation failed:', e);
                        }}
                    }}
                }}
            }}
            
            evaluateCondition(condition) {{
                // Simple condition evaluator
                try {{
                    // Replace variable names with values
                    let expr = condition;
                    for (let [key, value] of Object.entries(this.variables)) {{
                        expr = expr.replace(new RegExp(key, 'g'), JSON.stringify(value));
                    }}
                    return eval(expr);
                }} catch(e) {{
                    return false;
                }}
            }}
            
            updateReactiveUI() {{
                // Update any elements that depend on variables
                // This is a simplified reactive update
                for (let [id, element] of Object.entries(this.elements)) {{
                    if (element && element.type === 'input') {{
                        const value = this.variables[id];
                        if (value !== undefined && element.value !== value) {{
                            element.value = value;
                        }}
                    }}
                }}
            }}
        }}
        
        // Initialize runtime
        const runtime = new NovaRuntime();
        const runtimeData = {runtime_json};
        runtime.loadRuntime(runtimeData);
    </script>
</body>
</html>'''
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Generated runtime bundle: {output_path}")
        return True