# components.py
# Nova Programming Language - Component System
# Works in: Browser (with PyScript), Node.js, and Standard Python

import sys
import logging
from typing import Dict, List, Any, Optional, Callable, Union

# Set up logging
logger = logging.getLogger(__name__)

# ============ ENVIRONMENT DETECTION ============

class Environment:
    """Environment detection for components"""
    BROWSER = 'browser'
    NODE = 'node'
    PYTHON = 'python'
    UNKNOWN = 'unknown'

def detect_environment() -> str:
    """
    Detect the current execution environment.
    Uses multiple detection methods without importing browser modules.
    """
    # Method 1: Check for browser globals (most reliable)
    try:
        # This works in browsers and some Node.js environments
        # We use eval to avoid NameError
        if eval('typeof window !== "undefined" and window.document'):
            return Environment.BROWSER
    except:
        pass
    
    # Method 2: Check for document object
    try:
        # Try to access document safely
        if eval('typeof document !== "undefined"'):
            return Environment.BROWSER
    except:
        pass
    
    # Method 3: Check for navigator (browser-specific)
    try:
        if eval('typeof navigator !== "undefined" and navigator.userAgent'):
            return Environment.BROWSER
    except:
        pass
    
    # Method 4: Check if running in Node.js
    if hasattr(sys, 'argv') and len(sys.argv) > 0:
        if 'node' in sys.argv[0].lower():
            return Environment.NODE
        # Check for common Node.js indicators
        if hasattr(sys, 'version_info'):
            import platform
            if 'node' in platform.system().lower():
                return Environment.NODE
    
    # Method 5: Check for Python-specific indicators
    if hasattr(sys, 'implementation'):
        if sys.implementation.name == 'cpython':
            return Environment.PYTHON
    
    # Default to Python
    return Environment.PYTHON

# Detect environment once
ENV = detect_environment()

# ============ SAFE BROWSER API WRAPPERS ============

class BrowserAPI:
    """
    Safe wrapper for browser APIs.
    Provides fallbacks for non-browser environments.
    """
    
    @staticmethod
    def _get_browser_global(name: str, fallback: Any = None) -> Any:
        """Safely get a browser global without importing"""
        try:
            # Try eval first (works in browsers)
            result = eval(f'typeof {name} !== "undefined" ? {name} : null')
            if result is not None:
                return result
        except:
            pass
        
        try:
            # Try direct access (works in some environments)
            if name == 'document':
                import __main__
                if hasattr(__main__, 'document'):
                    return __main__.document
            elif name == 'window':
                import __main__
                if hasattr(__main__, 'window'):
                    return __main__.window
        except:
            pass
        
        return fallback
    
    @staticmethod
    def alert(message: str) -> None:
        """Show alert dialog or print fallback"""
        if ENV == Environment.BROWSER:
            try:
                # Try to use window.alert
                win = BrowserAPI._get_browser_global('window')
                if win and hasattr(win, 'alert'):
                    win.alert(str(message))
                    return
            except:
                pass
            
            try:
                # Try direct alert
                alert_func = BrowserAPI._get_browser_global('alert')
                if alert_func:
                    alert_func(str(message))
                    return
            except:
                pass
        
        # Fallback for non-browser environments
        logger.info(f"ALERT: {message}")
        print(f"🔔 ALERT: {message}")
    
    @staticmethod
    def confirm(message: str) -> bool:
        """Show confirm dialog or simulate"""
        if ENV == Environment.BROWSER:
            try:
                win = BrowserAPI._get_browser_global('window')
                if win and hasattr(win, 'confirm'):
                    return win.confirm(str(message))
            except:
                pass
            
            try:
                confirm_func = BrowserAPI._get_browser_global('confirm')
                if confirm_func:
                    return confirm_func(str(message))
            except:
                pass
        
        # Fallback for non-browser environments
        logger.info(f"CONFIRM: {message}")
        response = input(f"Confirm? (y/n): ").lower().strip()
        return response in ['y', 'yes', 'true', '1']
    
    @staticmethod
    def prompt(message: str, default: str = '') -> str:
        """Show prompt dialog or simulate"""
        if ENV == Environment.BROWSER:
            try:
                win = BrowserAPI._get_browser_global('window')
                if win and hasattr(win, 'prompt'):
                    return win.prompt(str(message), str(default))
            except:
                pass
            
            try:
                prompt_func = BrowserAPI._get_browser_global('prompt')
                if prompt_func:
                    return prompt_func(str(message), str(default))
            except:
                pass
        
        # Fallback for non-browser environments
        logger.info(f"PROMPT: {message}")
        return input(f"{message}: ")
    
    @staticmethod
    def get_document():
        """Get document object safely"""
        if ENV == Environment.BROWSER:
            try:
                win = BrowserAPI._get_browser_global('window')
                if win and hasattr(win, 'document'):
                    return win.document
            except:
                pass
            
            try:
                doc = BrowserAPI._get_browser_global('document')
                if doc:
                    return doc
            except:
                pass
        
        return None
    
    @staticmethod
    def get_window():
        """Get window object safely"""
        if ENV == Environment.BROWSER:
            try:
                win = BrowserAPI._get_browser_global('window')
                if win:
                    return win
            except:
                pass
        
        return None

# ============ SAFE FUNCTIONS ============

def safe_alert(message: str) -> None:
    """Show alert in browser or print in other environments"""
    BrowserAPI.alert(message)

def safe_confirm(message: str) -> bool:
    """Show confirm dialog in browser or simulate in other environments"""
    return BrowserAPI.confirm(message)

def safe_prompt(message: str, default: str = '') -> str:
    """Show prompt dialog in browser or simulate in other environments"""
    return BrowserAPI.prompt(message, default)

def get_document():
    """Get document object safely"""
    return BrowserAPI.get_document()

def get_window():
    """Get window object safely"""
    return BrowserAPI.get_window()

# ============ MOCK DOM FOR NON-BROWSER ============

class MockElement:
    """Mock DOM element for non-browser environments"""
    def __init__(self, tag: str = None):
        self.tag = tag
        self.children = []
        self.parentNode = None
        self.style = {}
        self.className = ''
        self.id = ''
        self.innerHTML = ''
        self.textContent = ''
        self.attributes = {}
        self._events = {}
        self._el = None
    
    def setAttribute(self, name: str, value: Any) -> None:
        self.attributes[name] = value
    
    def getAttribute(self, name: str) -> Any:
        return self.attributes.get(name)
    
    def removeAttribute(self, name: str) -> None:
        if name in self.attributes:
            del self.attributes[name]
    
    def appendChild(self, child: Any) -> Any:
        self.children.append(child)
        if hasattr(child, 'parentNode'):
            child.parentNode = self
        return child
    
    def removeChild(self, child: Any) -> Any:
        if child in self.children:
            self.children.remove(child)
            if hasattr(child, 'parentNode'):
                child.parentNode = None
        return child
    
    def replaceChild(self, new_child: Any, old_child: Any) -> Any:
        idx = self.children.index(old_child)
        self.children[idx] = new_child
        if hasattr(new_child, 'parentNode'):
            new_child.parentNode = self
        if hasattr(old_child, 'parentNode'):
            old_child.parentNode = None
        return old_child
    
    def addEventListener(self, event: str, handler: Callable) -> None:
        if event not in self._events:
            self._events[event] = []
        self._events[event].append(handler)
    
    def removeEventListener(self, event: str, handler: Callable) -> None:
        if event in self._events and handler in self._events[event]:
            self._events[event].remove(handler)
    
    def dispatchEvent(self, event: Any) -> None:
        if event in self._events:
            for handler in self._events[event]:
                handler(event)

class MockDocument:
    """Mock document for non-browser environments"""
    def __init__(self):
        self.body = MockElement('body')
        self.head = MockElement('head')
        self.documentElement = MockElement('html')
        self._elements = {}
    
    def createElement(self, tag: str) -> MockElement:
        return MockElement(tag)
    
    def createTextNode(self, text: str) -> dict:
        return {'type': 'text', 'content': text}
    
    def getElementById(self, id: str) -> Optional[MockElement]:
        return self._elements.get(id)
    
    def querySelector(self, selector: str) -> Optional[MockElement]:
        return None
    
    def querySelectorAll(self, selector: str) -> list:
        return []
    
    def getElementsByClassName(self, classname: str) -> list:
        return []
    
    def getElementsByTagName(self, tagname: str) -> list:
        return []
    
    def registerElement(self, id: str, element: MockElement) -> None:
        self._elements[id] = element

# ============ GET DOCUMENT INSTANCE ============

def get_document_instance():
    """Get document instance (real or mock)"""
    doc = get_document()
    if doc is not None:
        return doc
    return MockDocument()

document = get_document_instance()

# ============ COMPONENT REGISTRY ============

class ComponentRegistry:
    """Registry for Nova components"""
    
    def __init__(self):
        self.components: Dict[str, type] = {}
        self.styles: Dict[str, str] = {}
        self.scripts: Dict[str, str] = {}
    
    def register(self, name: str, component_class: type) -> None:
        """Register a component"""
        self.components[name] = component_class
    
    def get(self, name: str) -> Optional[type]:
        """Get a component by name"""
        return self.components.get(name)
    
    def register_style(self, name: str, styles: str) -> None:
        """Register component styles"""
        self.styles[name] = styles
    
    def register_script(self, name: str, script: str) -> None:
        """Register component script"""
        self.scripts[name] = script
    
    def list_components(self) -> List[str]:
        """List all registered components"""
        return list(self.components.keys())

# ============ BASE COMPONENT CLASS ============

class Component:
    """Base Nova Component - works in both browser and Python"""
    
    def __init__(self, props: Dict[str, Any] = None):
        self.props = props or {}
        self.name = self.__class__.__name__
        self._children = []
        self._mounted = False
        self._container = None
        self._state = {}
        self._env = ENV
        self._is_browser = ENV == Environment.BROWSER
        
        # Browser-specific properties
        if self._is_browser:
            self._vdom = None
            self._element = None
        
        # Lifecycle state
        self._lifecycle = {
            'mounting': False,
            'mounted': False,
            'updating': False,
            'unmounting': False
        }
        
        # Event handlers
        self._event_handlers = {}
    
    # ========== LIFECYCLE METHODS ==========
    
    def component_will_mount(self) -> None:
        """Called before component mounts"""
        pass
    
    def component_did_mount(self) -> None:
        """Called after component mounts"""
        pass
    
    def component_will_update(self) -> None:
        """Called before component updates"""
        pass
    
    def component_did_update(self) -> None:
        """Called after component updates"""
        pass
    
    def component_will_unmount(self) -> None:
        """Called before component unmounts"""
        pass
    
    def component_did_unmount(self) -> None:
        """Called after component unmounts"""
        pass
    
    # ========== STATE MANAGEMENT ==========
    
    def set_state(self, updates: Dict[str, Any]) -> None:
        """Update state and re-render"""
        old_state = self._state.copy()
        self._state = {**self._state, **updates}
        
        if self._mounted:
            self._update()
        
        # Notify state change listeners
        self._on_state_change(old_state, self._state)
    
    def get_state(self, key: str = None) -> Any:
        """Get state value"""
        if key is not None:
            return self._state.get(key)
        return self._state
    
    def _on_state_change(self, old_state: Dict, new_state: Dict) -> None:
        """Handle state change - override in subclasses"""
        pass
    
    # ========== RENDERING ==========
    
    def render(self) -> Any:
        """Render component - override in subclasses"""
        if self._is_browser:
            # In browser, return VDOM node
            try:
                from vdom import h
                return h('div', {'className': f'nova-component-{self.name}'}, 
                         f'Component: {self.name}')
            except ImportError:
                # vdom not available
                return {
                    'type': 'div',
                    'props': {'className': f'nova-component-{self.name}'},
                    'children': [f'Component: {self.name}']
                }
        else:
            # In Python, return dict representation
            return {
                'type': 'component',
                'name': self.name,
                'props': self.props,
                'state': self._state
            }
    
    def _render_browser(self) -> Any:
        """Render in browser environment"""
        return self.render()
    
    def _render_python(self) -> Dict:
        """Render in Python environment"""
        return self.render()
    
    # ========== MOUNTING ==========
    
    def mount(self, container: Any) -> None:
        """Mount component to DOM"""
        self._container = container
        self._lifecycle['mounting'] = True
        
        self.component_will_mount()
        
        if self._is_browser:
            self._mount_browser(container)
        else:
            self._mount_python(container)
        
        self._mounted = True
        self._lifecycle['mounting'] = False
        self._lifecycle['mounted'] = True
        
        self.component_did_mount()
    
    def _mount_browser(self, container: Any) -> None:
        """Mount in browser environment"""
        try:
            from vdom import VirtualDOM
            
            self._vdom = VirtualDOM()
            vnode = self._render_browser()
            self._element = self._vdom.render(vnode, container)
            
            # Store reference
            if hasattr(container, 'registerElement'):
                container.registerElement(self.name, self._element)
        except ImportError:
            # vdom not available - use fallback
            if hasattr(container, 'appendChild'):
                el = document.createElement('div')
                el.className = f'nova-component-{self.name}'
                el.textContent = f'Component: {self.name}'
                container.appendChild(el)
                self._element = el
    
    def _mount_python(self, container: Any) -> None:
        """Mount in Python environment"""
        # In Python, just store the render result
        self._element = self._render_python()
        if hasattr(container, 'appendChild'):
            container.appendChild(self._element)
    
    # ========== UPDATING ==========
    
    def _update(self) -> None:
        """Update component"""
        if not self._mounted:
            return
        
        self._lifecycle['updating'] = True
        self.component_will_update()
        
        if self._is_browser:
            self._update_browser()
        else:
            self._update_python()
        
        self._lifecycle['updating'] = False
        self.component_did_update()
    
    def _update_browser(self) -> None:
        """Update in browser environment"""
        if hasattr(self, '_vdom') and self._vdom and self._element:
            try:
                from vdom import VirtualDOM
                new_vnode = self._render_browser()
                patches = self._vdom.diff(self._vdom.old_tree, new_vnode)
                self._vdom.apply_patches(patches)
                self._vdom.old_tree = new_vnode
            except:
                # Fallback: simple replace
                if self._element and hasattr(self._element, 'parentNode'):
                    parent = self._element.parentNode
                    if parent:
                        new_el = document.createElement('div')
                        new_el.className = f'nova-component-{self.name}'
                        new_el.textContent = f'Component: {self.name} (updated)'
                        parent.replaceChild(new_el, self._element)
                        self._element = new_el
    
    def _update_python(self) -> None:
        """Update in Python environment"""
        self._element = self._render_python()
    
    # ========== UNMOUNTING ==========
    
    def unmount(self) -> None:
        """Unmount component"""
        if not self._mounted:
            return
        
        self._lifecycle['unmounting'] = True
        self.component_will_unmount()
        
        if self._is_browser:
            self._unmount_browser()
        else:
            self._unmount_python()
        
        self._mounted = False
        self._lifecycle['unmounting'] = False
        self._lifecycle['mounted'] = False
        
        self.component_did_unmount()
    
    def _unmount_browser(self) -> None:
        """Unmount in browser environment"""
        if self._element and hasattr(self._element, 'parentNode') and self._element.parentNode:
            self._element.parentNode.removeChild(self._element)
        self._element = None
        self._vdom = None
    
    def _unmount_python(self) -> None:
        """Unmount in Python environment"""
        self._element = None
    
    # ========== EVENT HANDLING ==========
    
    def on(self, event: str, handler: Callable) -> None:
        """Register event handler"""
        if event not in self._event_handlers:
            self._event_handlers[event] = []
        self._event_handlers[event].append(handler)
    
    def emit(self, event: str, data: Any = None) -> None:
        """Emit an event"""
        if event in self._event_handlers:
            for handler in self._event_handlers[event]:
                handler(data)
    
    # ========== UTILITY METHODS ==========
    
    def add_child(self, child: Any) -> 'Component':
        """Add a child component"""
        self._children.append(child)
        return self
    
    def get_children(self) -> List:
        """Get child components"""
        return self._children
    
    def find_child(self, name: str) -> Optional[Any]:
        """Find a child component by name"""
        for child in self._children:
            if hasattr(child, 'name') and child.name == name:
                return child
        return None
    
    # ========== RENDER HELPERS ==========
    
    def create_element(self, tag: str, props: Dict = None, *children) -> Any:
        """Create a DOM element (works in both environments)"""
        if self._is_browser:
            try:
                from vdom import h
                return h(tag, props, *children)
            except ImportError:
                return {
                    'type': 'element',
                    'tag': tag,
                    'props': props or {},
                    'children': list(children)
                }
        else:
            return {
                'type': 'element',
                'tag': tag,
                'props': props or {},
                'children': list(children)
            }
    
    def create_text(self, content: str) -> Any:
        """Create a text node"""
        if self._is_browser:
            try:
                from vdom import text
                return text(content)
            except ImportError:
                return {'type': 'text', 'content': content}
        else:
            return {'type': 'text', 'content': content}
    
    def create_fragment(self, *children) -> Any:
        """Create a fragment"""
        if self._is_browser:
            try:
                from vdom import fragment
                return fragment(*children)
            except ImportError:
                return {'type': 'fragment', 'children': list(children)}
        else:
            return {'type': 'fragment', 'children': list(children)}
    
    # ========== ALERT HELPERS ==========
    
    def show_alert(self, message: str) -> None:
        """Show alert using safe wrapper"""
        safe_alert(message)
    
    def show_confirm(self, message: str) -> bool:
        """Show confirm using safe wrapper"""
        return safe_confirm(message)
    
    def show_prompt(self, message: str, default: str = '') -> str:
        """Show prompt using safe wrapper"""
        return safe_prompt(message, default)

# ============ DYNAMIC COMPONENT ============

def create_component(
    name: str,
    render_fn: Callable,
    state: Dict = None,
    props: Dict = None
) -> type:
    """Create a component from a render function"""
    
    class DynamicComponent(Component):
        def __init__(self, props=None):
            super().__init__(props)
            if state:
                self._state = state.copy()
            self._render_fn = render_fn
        
        def render(self):
            return self._render_fn(self.props, self._state, self.set_state)
    
    DynamicComponent.__name__ = name
    return DynamicComponent

# ============ COMPONENT FROM AST ============

def component_from_ast(ast_node: Any, registry: ComponentRegistry) -> Optional[type]:
    """Create a component from AST node"""
    if not hasattr(ast_node, 'node_type') or ast_node.node_type != 'Component':
        return None
    
    component_name = getattr(ast_node, 'name', 'Anonymous')
    
    def render_fn(props, state, set_state):
        """Render function for component"""
        if ENV == Environment.BROWSER:
            try:
                from vdom import h
                children = []
                for child in getattr(ast_node, 'body', []):
                    child_node = node_to_component(child, registry)
                    if child_node:
                        children.append(child_node)
                
                return h('div', {'className': f'nova-component-{component_name}'}, *children)
            except ImportError:
                return {
                    'type': 'div',
                    'props': {'className': f'nova-component-{component_name}'},
                    'children': [str(child) for child in getattr(ast_node, 'body', [])]
                }
        else:
            return {
                'type': 'component',
                'name': component_name,
                'children': getattr(ast_node, 'body', [])
            }
    
    return create_component(
        component_name,
        render_fn,
        state=getattr(ast_node, 'state', {}),
        props=getattr(ast_node, 'props', {})
    )

# ============ NODE TO COMPONENT ============

def node_to_component(node: Any, registry: ComponentRegistry) -> Any:
    """Convert an AST node to a component"""
    if not hasattr(node, 'node_type'):
        return None
    
    if ENV == Environment.BROWSER:
        try:
            from vdom import h
            
            if node.node_type == 'Button':
                button_name = getattr(node, 'name', 'button')
                button_text = getattr(node, 'text', button_name)
                
                def on_click():
                    safe_alert(f"Button {button_name} clicked")
                
                return h('button', {
                    'className': 'nova-button',
                    'id': button_name,
                    'onClick': on_click
                }, button_text)
            
            elif node.node_type == 'Text':
                return h('p', {'className': 'nova-text'}, getattr(node, 'content', ''))
            
            elif node.node_type == 'Heading':
                return h('h1', {'className': 'nova-heading'}, getattr(node, 'content', ''))
            
            elif node.node_type == 'Subtitle':
                return h('h2', {'className': 'nova-subtitle'}, getattr(node, 'content', ''))
            
            elif node.node_type == 'Input':
                name = getattr(node, 'name', 'input')
                return h('div', {'className': 'nova-input-group'},
                    h('label', {'className': 'nova-label', 'htmlFor': name}, name),
                    h('input', {
                        'type': 'text',
                        'id': name,
                        'className': 'nova-input',
                        'placeholder': getattr(node, 'placeholder', '')
                    })
                )
            
            elif node.node_type == 'NumberInput':
                name = getattr(node, 'name', 'number')
                return h('div', {'className': 'nova-input-group'},
                    h('label', {'className': 'nova-label', 'htmlFor': name}, name),
                    h('input', {
                        'type': 'number',
                        'id': name,
                        'className': 'nova-input',
                        'value': getattr(node, 'value', 0)
                    })
                )
            
            elif node.node_type == 'Checkbox':
                name = getattr(node, 'name', 'checkbox')
                checked = getattr(node, 'checked', False)
                return h('div', {'className': 'nova-checkbox-group'},
                    h('input', {
                        'type': 'checkbox',
                        'id': name,
                        'className': 'nova-checkbox',
                        'checked': checked
                    }),
                    h('label', {'className': 'nova-label', 'htmlFor': name}, 
                      getattr(node, 'label', name))
                )
            
            elif node.node_type == 'Dropdown':
                name = getattr(node, 'name', 'dropdown')
                options = getattr(node, 'options', [])
                selected = getattr(node, 'selected', '')
                
                opt_elements = []
                for option in options:
                    opt_elements.append(h('option', {
                        'value': option,
                        'selected': option == selected
                    }, option))
                
                return h('div', {'className': 'nova-input-group'},
                    h('label', {'className': 'nova-label', 'htmlFor': name}, name),
                    h('select', {'id': name, 'className': 'nova-dropdown'}, *opt_elements)
                )
            
            elif node.node_type == 'Container':
                children = []
                for child in getattr(node, 'children', []):
                    child_node = node_to_component(child, registry)
                    if child_node:
                        children.append(child_node)
                return h('div', {'className': 'nova-container'}, *children)
            
            elif node.node_type == 'Card':
                children = []
                title = getattr(node, 'title', '')
                if title:
                    children.append(h('h3', {'className': 'nova-card-title'}, title))
                for child in getattr(node, 'children', []):
                    child_node = node_to_component(child, registry)
                    if child_node:
                        children.append(child_node)
                return h('div', {'className': 'nova-card'}, *children)
            
            elif node.node_type == 'Section':
                children = []
                title = getattr(node, 'title', '')
                if title:
                    children.append(h('h2', {'className': 'nova-section-title'}, title))
                for child in getattr(node, 'children', []):
                    child_node = node_to_component(child, registry)
                    if child_node:
                        children.append(child_node)
                return h('section', {'className': 'nova-section'}, *children)
            
            elif node.node_type == 'Use':
                component = registry.get(getattr(node, 'name', ''))
                if component:
                    return h(component, {})
                return None
            
            elif node.node_type == 'Link':
                return h('a', {
                    'className': 'nova-link',
                    'href': getattr(node, 'url', '#')
                }, getattr(node, 'text', 'Link'))
            
            elif node.node_type == 'Image':
                return h('img', {
                    'className': 'nova-image',
                    'src': getattr(node, 'src', ''),
                    'alt': getattr(node, 'alt', 'Image')
                })
            
            elif node.node_type == 'Video':
                return h('video', {
                    'className': 'nova-video',
                    'src': getattr(node, 'src', ''),
                    'controls': True
                })
            
            elif node.node_type == 'Audio':
                return h('audio', {
                    'className': 'nova-audio',
                    'src': getattr(node, 'src', ''),
                    'controls': True
                })
        
        except ImportError:
            # vdom not available - return dict
            return {
                'type': 'node',
                'node_type': node.node_type,
                'properties': vars(node) if hasattr(node, '__dict__') else {}
            }
    
    # Python environment - return dict representation
    else:
        return {
            'type': 'node',
            'node_type': node.node_type,
            'properties': vars(node) if hasattr(node, '__dict__') else {}
        }

# ============ RENDER COMPONENTS ============

def render_components(ast: List[Any], registry: ComponentRegistry) -> List[Any]:
    """Render all components in AST"""
    components = []
    
    for node in ast:
        if hasattr(node, 'node_type'):
            if node.node_type == 'Component':
                comp = component_from_ast(node, registry)
                if comp:
                    registry.register(getattr(node, 'name', 'Anonymous'), comp)
            elif node.node_type == 'Use':
                comp = registry.get(getattr(node, 'name', ''))
                if comp:
                    components.append(comp)
            elif hasattr(node, 'children'):
                components.extend(render_components(node.children, registry))
    
    return components

# ============ COMPONENT STYLES ============

def get_component_styles(registry: ComponentRegistry) -> str:
    """Get all component styles as CSS"""
    css = "/* Component Styles */\n\n"
    for name, styles in registry.styles.items():
        css += f"/* {name} */\n"
        css += styles
        css += "\n"
    return css

# ============ COMPONENT SCRIPTS ============

def get_component_scripts(registry: ComponentRegistry) -> str:
    """Get all component scripts as JavaScript"""
    js = "// Component Scripts\n\n"
    for name, script in registry.scripts.items():
        js += f"// {name}\n"
        js += script
        js += "\n"
    return js

# ============ EXPORTS ============

__all__ = [
    'Component',
    'ComponentRegistry',
    'create_component',
    'component_from_ast',
    'node_to_component',
    'render_components',
    'get_component_styles',
    'get_component_scripts',
    'safe_alert',
    'safe_confirm',
    'safe_prompt',
    'get_document',
    'get_window',
    'ENV',
    'Environment'
]