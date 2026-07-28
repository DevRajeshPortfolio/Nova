# vdom.py
# Nova Programming Language - Virtual DOM Implementation
# Works in: Browser, Node.js, and Standard Python

import sys
import time
import threading
import logging
from typing import Any, Dict, List, Optional, Union, Callable

# Set up logging
logger = logging.getLogger(__name__)

# ============ ENVIRONMENT DETECTION ============

class Environment:
    """Environment detection for VDOM"""
    BROWSER = 'browser'
    NODE = 'node'
    PYTHON = 'python'
    UNKNOWN = 'unknown'

def detect_environment() -> str:
    """
    Detect the current execution environment.
    Uses multiple detection methods without importing browser modules.
    """
    # Method 1: Check for browser globals using eval
    try:
        if eval('typeof window !== "undefined" && window.document'):
            return Environment.BROWSER
    except:
        pass
    
    # Method 2: Check for document object
    try:
        if eval('typeof document !== "undefined"'):
            return Environment.BROWSER
    except:
        pass
    
    # Method 3: Check for navigator
    try:
        if eval('typeof navigator !== "undefined"'):
            return Environment.BROWSER
    except:
        pass
    
    # Method 4: Check if running in Node.js
    if hasattr(sys, 'argv') and len(sys.argv) > 0:
        if 'node' in sys.argv[0].lower():
            return Environment.NODE
    
    # Method 5: Check for Python-specific indicators
    if hasattr(sys, 'implementation'):
        if sys.implementation.name == 'cpython':
            return Environment.PYTHON
    
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
            result = eval(f'typeof {name} !== "undefined" ? {name} : null')
            if result is not None:
                return result
        except:
            pass
        
        try:
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
    
    @staticmethod
    def get_request_animation_frame():
        """Get requestAnimationFrame function safely"""
        if ENV == Environment.BROWSER:
            try:
                win = BrowserAPI._get_browser_global('window')
                if win and hasattr(win, 'requestAnimationFrame'):
                    return win.requestAnimationFrame
            except:
                pass
            
            try:
                raf = BrowserAPI._get_browser_global('requestAnimationFrame')
                if raf:
                    return raf
            except:
                pass
        
        return None
    
    @staticmethod
    def get_cancel_animation_frame():
        """Get cancelAnimationFrame function safely"""
        if ENV == Environment.BROWSER:
            try:
                win = BrowserAPI._get_browser_global('window')
                if win and hasattr(win, 'cancelAnimationFrame'):
                    return win.cancelAnimationFrame
            except:
                pass
            
            try:
                caf = BrowserAPI._get_browser_global('cancelAnimationFrame')
                if caf:
                    return caf
            except:
                pass
        
        return None

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
    
    def __repr__(self):
        return f"MockElement({self.tag}, id={self.id}, className={self.className})"

class MockDocument:
    """Mock document for non-browser environments"""
    def __init__(self):
        self.body = MockElement('body')
        self.head = MockElement('head')
        self.documentElement = MockElement('html')
        self._elements = {}
        self._element_count = 0
    
    def createElement(self, tag: str) -> MockElement:
        """Create a mock element"""
        return MockElement(tag)
    
    def createTextNode(self, text: str) -> dict:
        """Create a text node"""
        return {'type': 'text', 'content': text, 'textContent': text}
    
    def getElementById(self, id: str) -> Optional[MockElement]:
        """Get element by ID"""
        return self._elements.get(id)
    
    def querySelector(self, selector: str) -> Optional[MockElement]:
        """Query selector (mock implementation)"""
        # Simple mock - just check if selector matches any registered element
        if selector.startswith('#'):
            return self._elements.get(selector[1:])
        return None
    
    def querySelectorAll(self, selector: str) -> list:
        """Query all selectors (mock implementation)"""
        results = []
        if selector.startswith('.'):
            classname = selector[1:]
            for element in self._elements.values():
                if element.className == classname:
                    results.append(element)
        elif selector.startswith('#'):
            element = self._elements.get(selector[1:])
            if element:
                results.append(element)
        return results
    
    def getElementsByClassName(self, classname: str) -> list:
        """Get elements by class name"""
        results = []
        for element in self._elements.values():
            if element.className == classname:
                results.append(element)
        return results
    
    def getElementsByTagName(self, tagname: str) -> list:
        """Get elements by tag name"""
        results = []
        for element in self._elements.values():
            if element.tag == tagname:
                results.append(element)
        return results
    
    def registerElement(self, id: str, element: MockElement) -> None:
        """Register an element by ID"""
        self._elements[id] = element
        element.id = id
    
    def createEvent(self, event_type: str) -> dict:
        """Create a mock event"""
        return {
            'type': event_type,
            'target': None,
            'preventDefault': lambda: None,
            'stopPropagation': lambda: None
        }

# ============ GET DOCUMENT INSTANCE ============

def get_document_instance():
    """Get document instance (real or mock)"""
    doc = BrowserAPI.get_document()
    if doc is not None:
        return doc
    return MockDocument()

# Create global document instance
document = get_document_instance()

# ============ REQUEST ANIMATION FRAME ============

class AnimationManager:
    """
    Animation frame manager for any environment.
    Uses native requestAnimationFrame in browsers, fallback in others.
    """
    
    def __init__(self):
        self._callbacks: Dict[int, Callable] = {}
        self._next_id = 0
        self._running = False
        self._thread = None
        self._lock = threading.Lock()
        self._env = ENV
        self._raf = BrowserAPI.get_request_animation_frame()
        self._caf = BrowserAPI.get_cancel_animation_frame()
        self._use_native = self._raf is not None
        self._frame_interval = 1.0 / 60.0  # 60fps default
    
    def requestAnimationFrame(self, callback: Callable) -> int:
        """
        Request an animation frame.
        Uses native browser API if available, otherwise uses threading.
        """
        # Try native browser API first
        if self._use_native and self._raf is not None:
            try:
                # Some browsers need the callback to be bound
                result = self._raf(callback)
                if result is not None:
                    return result
            except Exception as e:
                logger.debug(f"Native requestAnimationFrame failed: {e}")
                self._use_native = False
        
        # Fallback for non-browser environments
        with self._lock:
            self._next_id += 1
            frame_id = self._next_id
            self._callbacks[frame_id] = callback
        
        # Start the animation loop if not running
        if not self._running:
            self._start_loop()
        
        return frame_id
    
    def cancelAnimationFrame(self, frame_id: int) -> None:
        """Cancel an animation frame"""
        # Try native browser API first
        if self._use_native and self._caf is not None:
            try:
                self._caf(frame_id)
                return
            except Exception as e:
                logger.debug(f"Native cancelAnimationFrame failed: {e}")
                self._use_native = False
        
        # Fallback for non-browser environments
        with self._lock:
            if frame_id in self._callbacks:
                del self._callbacks[frame_id]
    
    def _start_loop(self) -> None:
        """Start the animation loop in a background thread"""
        self._running = True
        
        def loop():
            while self._running:
                start_time = time.time()
                
                # Get current callbacks
                with self._lock:
                    callbacks = dict(self._callbacks)
                    self._callbacks.clear()
                
                # Execute callbacks
                current_time = time.time()
                for frame_id, callback in callbacks.items():
                    try:
                        callback(current_time)
                    except Exception as e:
                        logger.error(f"Animation callback error (frame {frame_id}): {e}")
                
                # Calculate sleep time to maintain frame rate
                elapsed = time.time() - start_time
                sleep_time = max(0, self._frame_interval - elapsed)
                if sleep_time > 0:
                    time.sleep(sleep_time)
        
        self._thread = threading.Thread(target=loop, daemon=True)
        self._thread.start()
    
    def stop(self) -> None:
        """Stop the animation loop"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=1.0)
        with self._lock:
            self._callbacks.clear()
    
    def set_frame_rate(self, fps: float) -> None:
        """Set the frame rate for the animation loop"""
        self._frame_interval = 1.0 / fps

# Create global animation manager
_anim_manager = AnimationManager()

def requestAnimationFrame(callback: Callable) -> int:
    """
    Request an animation frame.
    Works in browser, Node.js, and Python.
    """
    return _anim_manager.requestAnimationFrame(callback)

def cancelAnimationFrame(frame_id: int) -> None:
    """
    Cancel an animation frame.
    Works in browser, Node.js, and Python.
    """
    _anim_manager.cancelAnimationFrame(frame_id)

def set_animation_frame_rate(fps: float) -> None:
    """Set the animation frame rate"""
    _anim_manager.set_frame_rate(fps)

# ============ VDOM NODE CLASS ============

class VDOMNode:
    """Virtual DOM Node"""
    
    def __init__(self, tag: str, props: Dict = None, children: List = None):
        self.tag = tag
        self.props = props or {}
        self.children = children or []
        self.key = self.props.get('key')
        self._el = None  # Reference to real DOM element
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            'tag': self.tag,
            'props': self.props,
            'children': [c.to_dict() if isinstance(c, VDOMNode) else c for c in self.children]
        }
    
    def __repr__(self) -> str:
        return f"VDOMNode({self.tag}, props={self.props}, children={len(self.children)})"

# ============ VIRTUAL DOM CLASS ============

class VirtualDOM:
    """Virtual DOM Engine with Diffing and Patching"""
    
    def __init__(self):
        self.old_tree = None
        self.new_tree = None
        self.root_element = None
        self.patches = []
        self.update_queue = []
        self.is_batching = False
        self._update_scheduled = False
        self._env = ENV
        self._is_browser = ENV == Environment.BROWSER
        
        # Get document instance
        self._document = get_document_instance()
        self._element_cache = {}
    
    # ========== ELEMENT CREATION ==========
    
    def create_element(self, vnode: Union[VDOMNode, str]) -> Any:
        """Create a real DOM element from a virtual node"""
        # Handle text nodes
        if isinstance(vnode, str):
            if self._is_browser:
                return self._document.createTextNode(vnode)
            else:
                return MockElement('text')
        
        # Handle text-like objects
        if hasattr(vnode, 'get') and vnode.get('type') == 'text':
            if self._is_browser:
                return self._document.createTextNode(vnode.get('content', ''))
            else:
                return MockElement('text')
        
        # Ensure it's a VDOMNode
        if not isinstance(vnode, VDOMNode):
            vnode = VDOMNode('div', {}, [str(vnode)])
        
        # Create element based on environment
        if self._is_browser:
            return self._create_browser_element(vnode)
        else:
            return self._create_mock_element(vnode)
    
    def _create_browser_element(self, vnode: VDOMNode) -> Any:
        """Create a real browser DOM element"""
        try:
            # Create element
            el = self._document.createElement(vnode.tag)
            
            # Set properties and attributes
            for key, value in vnode.props.items():
                if key.startswith('on') and callable(value):
                    # Event handler
                    event_name = key[2:].lower()
                    el.addEventListener(event_name, value)
                elif key == 'className':
                    el.className = value
                elif key == 'style' and isinstance(value, dict):
                    for style_key, style_value in value.items():
                        try:
                            el.style[style_key] = style_value
                        except:
                            # Some style properties might not be writable
                            pass
                elif key in ['id', 'type', 'href', 'src', 'alt', 'value', 
                            'placeholder', 'checked', 'disabled', 'readonly']:
                    try:
                        el.setAttribute(key, value)
                    except:
                        pass
                else:
                    try:
                        el.setAttribute(key, value)
                    except:
                        pass
            
            # Render children
            for child in vnode.children:
                child_el = self.create_element(child)
                try:
                    el.appendChild(child_el)
                except Exception as e:
                    logger.warning(f"Failed to append child: {e}")
            
            # Store reference
            vnode._el = el
            
            # Cache by ID if present
            if vnode.props.get('id'):
                self._element_cache[vnode.props['id']] = el
            
            return el
            
        except Exception as e:
            logger.error(f"Error creating browser element: {e}")
            # Fallback: create a div with text content
            fallback_el = self._document.createElement('div')
            fallback_el.textContent = f"Error: {e}"
            return fallback_el
    
    def _create_mock_element(self, vnode: VDOMNode) -> MockElement:
        """Create a mock element for non-browser environments"""
        el = MockElement(vnode.tag)
        
        # Set attributes
        for key, value in vnode.props.items():
            if key == 'className':
                el.className = value
            elif key == 'id':
                el.id = value
            elif key == 'style' and isinstance(value, dict):
                el.style = value
            elif key in ['type', 'href', 'src', 'alt', 'value', 'placeholder']:
                el.setAttribute(key, value)
            else:
                el.setAttribute(key, value)
        
        # Render children
        for child in vnode.children:
            child_el = self.create_element(child)
            el.appendChild(child_el)
        
        # Store reference
        vnode._el = el
        
        # Register by ID if present
        if vnode.props.get('id'):
            if hasattr(self._document, 'registerElement'):
                self._document.registerElement(vnode.props['id'], el)
            self._element_cache[vnode.props['id']] = el
        
        return el
    
    # ========== RENDERING ==========
    
    def render(self, vnode: Union[VDOMNode, str], container: Any) -> Any:
        """Render a virtual DOM tree to a container"""
        self.root_element = container
        self.old_tree = vnode
        
        try:
            # Clear container
            if self._is_browser and hasattr(container, 'innerHTML'):
                container.innerHTML = ''
            elif hasattr(container, 'children'):
                container.children = []
            
            # Create and append element
            el = self.create_element(vnode)
            
            if hasattr(container, 'appendChild'):
                container.appendChild(el)
            elif hasattr(container, 'innerHTML') and not self._is_browser:
                # For non-browser with innerHTML but no appendChild
                if hasattr(el, 'outerHTML'):
                    container.innerHTML = el.outerHTML
                else:
                    container.innerHTML = str(el)
            
            return el
            
        except Exception as e:
            logger.error(f"Error rendering VDOM: {e}")
            return None
    
    # ========== DIFFING ==========
    
    def diff(self, old_node: Optional[Union[VDOMNode, str]], 
             new_node: Optional[Union[VDOMNode, str]]) -> List[Dict]:
        """Calculate differences between two VDOM trees"""
        patches = []
        
        # Handle None cases
        if old_node is None and new_node is not None:
            patches.append({'type': 'create', 'node': new_node})
            return patches
        
        if old_node is not None and new_node is None:
            patches.append({'type': 'remove', 'node': old_node})
            return patches
        
        if old_node is None and new_node is None:
            return patches
        
        # Handle text nodes
        if isinstance(old_node, str) and isinstance(new_node, str):
            if old_node != new_node:
                patches.append({'type': 'replace_text', 'old': old_node, 'new': new_node})
            return patches
        
        if isinstance(old_node, str) or isinstance(new_node, str):
            patches.append({'type': 'replace', 'old': old_node, 'new': new_node})
            return patches
        
        # Ensure both are VDOMNode
        if not isinstance(old_node, VDOMNode):
            old_node = VDOMNode('div', {}, [str(old_node)])
        if not isinstance(new_node, VDOMNode):
            new_node = VDOMNode('div', {}, [str(new_node)])
        
        # Different tags - replace
        if old_node.tag != new_node.tag:
            patches.append({'type': 'replace', 'old': old_node, 'new': new_node})
            return patches
        
        # Diff props
        prop_patches = self._diff_props(old_node.props, new_node.props)
        if prop_patches:
            patches.append({'type': 'props', 'patches': prop_patches})
        
        # Diff children using key-based reconciliation
        child_patches = self._diff_children(old_node.children, new_node.children)
        patches.extend(child_patches)
        
        return patches
    
    def _diff_props(self, old_props: Dict, new_props: Dict) -> List[Dict]:
        """Diff properties between two nodes"""
        patches = []
        
        # Check for changed or removed props
        for key in old_props:
            if key not in new_props:
                patches.append({'type': 'remove_prop', 'key': key})
            elif old_props[key] != new_props[key]:
                patches.append({'type': 'set_prop', 'key': key, 'value': new_props[key]})
        
        # Check for added props
        for key in new_props:
            if key not in old_props:
                patches.append({'type': 'set_prop', 'key': key, 'value': new_props[key]})
        
        return patches
    
    def _diff_children(self, old_children: List, new_children: List) -> List[Dict]:
        """Diff children with key support"""
        patches = []
        
        # Build key maps for efficient diffing
        old_keys = {}
        new_keys = {}
        
        for i, child in enumerate(old_children):
            if isinstance(child, VDOMNode) and child.key:
                old_keys[child.key] = i
        
        for i, child in enumerate(new_children):
            if isinstance(child, VDOMNode) and child.key:
                new_keys[child.key] = i
        
        # Simple diff: iterate through children
        max_len = max(len(old_children), len(new_children))
        for i in range(max_len):
            old_child = old_children[i] if i < len(old_children) else None
            new_child = new_children[i] if i < len(new_children) else None
            
            if old_child is None and new_child is not None:
                patches.append({'type': 'add', 'index': i, 'node': new_child})
            elif old_child is not None and new_child is None:
                patches.append({'type': 'remove_at', 'index': i, 'node': old_child})
            elif old_child is not None and new_child is not None:
                child_patches = self.diff(old_child, new_child)
                if child_patches:
                    for patch in child_patches:
                        patch['index'] = i
                    patches.extend(child_patches)
        
        return patches
    
    # ========== PATCHING ==========
    
    def apply_patches(self, patches: List[Dict], node: Any = None) -> None:
        """Apply patches to real DOM"""
        if not patches:
            return
        
        if node is None:
            node = self.root_element
        
        if not node:
            return
        
        for patch in patches:
            try:
                self._apply_patch(patch, node)
            except Exception as e:
                logger.warning(f"Failed to apply patch {patch}: {e}")
    
    def _apply_patch(self, patch: Dict, node: Any) -> None:
        """Apply a single patch"""
        patch_type = patch.get('type')
        
        if patch_type == 'create':
            # Create new node and append
            new_el = self.create_element(patch['node'])
            if hasattr(node, 'appendChild'):
                node.appendChild(new_el)
            elif hasattr(node, 'children'):
                node.children.append(new_el)
        
        elif patch_type == 'remove':
            # Remove node
            el = patch['node']._el if hasattr(patch['node'], '_el') else None
            if el and hasattr(el, 'parentNode') and el.parentNode:
                el.parentNode.removeChild(el)
            elif hasattr(node, 'children') and patch['node'] in node.children:
                node.children.remove(patch['node'])
        
        elif patch_type == 'remove_at':
            # Remove node at index
            idx = patch.get('index', 0)
            if hasattr(node, 'children') and idx < len(node.children):
                if self._is_browser:
                    node.removeChild(node.children[idx])
                else:
                    node.children.pop(idx)
            elif self._is_browser and hasattr(node, 'childNodes') and idx < node.childNodes.length:
                node.removeChild(node.childNodes[idx])
        
        elif patch_type == 'replace':
            # Replace node
            old_el = patch['old']._el if hasattr(patch['old'], '_el') else None
            new_el = self.create_element(patch['new'])
            if old_el and hasattr(old_el, 'parentNode') and old_el.parentNode:
                old_el.parentNode.replaceChild(new_el, old_el)
            elif hasattr(node, 'children') and patch['old'] in node.children:
                idx = node.children.index(patch['old'])
                node.children[idx] = new_el
        
        elif patch_type == 'replace_text':
            # Replace text
            if self._is_browser and hasattr(node, 'textContent'):
                node.textContent = patch['new']
            elif hasattr(node, 'content'):
                node.content = patch['new']
        
        elif patch_type == 'add':
            # Add child at index
            idx = patch.get('index', 0)
            new_el = self.create_element(patch['node'])
            if self._is_browser:
                if hasattr(node, 'childNodes') and idx < node.childNodes.length:
                    node.insertBefore(new_el, node.childNodes[idx])
                else:
                    node.appendChild(new_el)
            elif hasattr(node, 'children'):
                if idx < len(node.children):
                    node.children.insert(idx, new_el)
                else:
                    node.children.append(new_el)
        
        elif patch_type == 'props':
            # Apply property changes
            for prop_patch in patch.get('patches', []):
                self._apply_prop_patch(prop_patch, node)
    
    def _apply_prop_patch(self, prop_patch: Dict, node: Any) -> None:
        """Apply a property patch"""
        prop_type = prop_patch.get('type')
        key = prop_patch.get('key')
        value = prop_patch.get('value')
        
        if prop_type == 'set_prop':
            if key == 'className':
                if hasattr(node, 'className'):
                    node.className = value
                else:
                    node.setAttribute('class', value)
            elif key == 'style' and isinstance(value, dict):
                if hasattr(node, 'style'):
                    for style_key, style_value in value.items():
                        node.style[style_key] = style_value
            elif hasattr(node, 'setAttribute'):
                node.setAttribute(key, value)
            elif hasattr(node, 'attributes'):
                node.attributes[key] = value
        
        elif prop_type == 'remove_prop':
            if key == 'className':
                if hasattr(node, 'className'):
                    node.className = ''
            elif hasattr(node, 'removeAttribute'):
                node.removeAttribute(key)
            elif hasattr(node, 'attributes') and key in node.attributes:
                del node.attributes[key]
    
    # ========== BATCH UPDATES ==========
    
    def batch_update(self, updates: List[Dict]) -> None:
        """Batch multiple updates together"""
        self.is_batching = True
        self.update_queue.extend(updates)
        
        if not self._update_scheduled:
            self._update_scheduled = True
            # Schedule flush
            try:
                requestAnimationFrame(self._flush_updates)
            except:
                # Fallback: flush immediately
                self._flush_updates()
    
    def _flush_updates(self, timestamp: float = None) -> None:
        """Flush all batched updates"""
        self.is_batching = False
        self._update_scheduled = False
        
        # Apply all updates
        for update in self.update_queue:
            self.apply_patches(update.get('patches', []), update.get('node'))
        
        self.update_queue = []
    
    # ========== REACTIVE STATE ==========
    
    def create_reactive_state(self, initial_state: Dict = None, 
                             on_change: Callable = None) -> Dict:
        """Create reactive state with automatic updates"""
        state = initial_state.copy() if initial_state else {}
        subscribers = []
        
        def set_state(updates: Dict) -> None:
            nonlocal state
            old_state = state.copy()
            state = {**state, **updates}
            
            if on_change:
                on_change(state, old_state)
            
            # Notify subscribers
            for sub in subscribers:
                try:
                    sub(state, old_state)
                except Exception as e:
                    logger.error(f"State subscriber error: {e}")
        
        def get_state(key: str = None) -> Any:
            if key is not None:
                return state.get(key)
            return state
        
        def subscribe(callback: Callable) -> Callable:
            subscribers.append(callback)
            return lambda: subscribers.remove(callback) if callback in subscribers else None
        
        return {
            'get': get_state,
            'set': set_state,
            'subscribe': subscribe,
            'state': state
        }
    
    # ========== UTILITY METHODS ==========
    
    def get_element_by_id(self, element_id: str) -> Any:
        """Get element by ID"""
        if self._is_browser:
            return self._document.getElementById(element_id)
        return self._element_cache.get(element_id)
    
    def get_element_cache(self) -> Dict:
        """Get element cache"""
        return self._element_cache
    
    def clear_cache(self) -> None:
        """Clear element cache"""
        self._element_cache = {}

# ============ UTILITY FUNCTIONS ============

def h(tag: str, props: Dict = None, *children) -> VDOMNode:
    """Create a VDOM node (hyperscript style)"""
    return VDOMNode(tag, props or {}, list(children))

def fragment(*children) -> VDOMNode:
    """Create a fragment (group of children without wrapper)"""
    return VDOMNode('fragment', {}, list(children))

def text(content: str) -> str:
    """Create a text node"""
    return content

def create_vdom_from_dict(data: Dict) -> VDOMNode:
    """Create a VDOM node from a dictionary"""
    if isinstance(data, dict):
        tag = data.get('tag', 'div')
        props = data.get('props', {})
        children = data.get('children', [])
        return VDOMNode(tag, props, [create_vdom_from_dict(c) for c in children])
    return data

# ============ EXPORTS ============

__all__ = [
    'VDOMNode',
    'VirtualDOM',
    'h',
    'fragment',
    'text',
    'create_vdom_from_dict',
    'requestAnimationFrame',
    'cancelAnimationFrame',
    'set_animation_frame_rate',
    'get_document_instance',
    'document',
    'ENV',
    'Environment'
]