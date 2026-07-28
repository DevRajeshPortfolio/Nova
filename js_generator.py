# js_generator.py
# Nova Programming Language - JavaScript Generator

import json

class JSGenerator:
    def __init__(self):
        self.js = ''
        self.variables = {}
        self.event_handlers = []
        self.actions = {}
        self.components = {}
        self.states = {}
        self.lists = {}
    
    def generate(self, ast):
        """Generate JavaScript from AST"""
        self.js = '// Nova Generated JavaScript\n\n'
        
        # First pass: collect variables, actions, components, states
        for node in ast:
            self.collect_declarations(node)
        
        # Generate state management
        self.js += self.generate_state_management()
        
        self.js += 'document.addEventListener("DOMContentLoaded", function() {\n'
        
        # Generate component rendering
        self.js += self.generate_component_rendering(ast)
        
        # Generate code
        for node in ast:
            self.generate_node(node)
        
        # Generate event handlers
        self.js += self.generate_event_handlers(ast)
        
        # Add slideshow functionality
        self.js += self.generate_slideshow_js(ast)
        
        # Add tabs functionality
        self.js += self.generate_tabs_js(ast)
        
        # Add mouse position tracking
        self.js += self.generate_mouse_js(ast)
        
        # Add keyboard tracking
        self.js += self.generate_keyboard_js(ast)
        
        # Add touch tracking
        self.js += self.generate_touch_js(ast)
        
        # Add device event tracking
        self.js += self.generate_device_js(ast)
        
        self.js += '});\n'
        
        # Generate action functions
        self.js += self.generate_actions()
        
        return self.js
    
    def collect_declarations(self, node):
        """Collect declarations from AST"""
        if node.node_type == 'NumberInput':
            self.variables[node.name] = 0
        elif node.node_type == 'Input':
            self.variables[node.name] = ''
        elif node.node_type == 'Password':
            self.variables[node.name] = ''
        elif node.node_type == 'Email':
            self.variables[node.name] = ''
        elif node.node_type == 'Search':
            self.variables[node.name] = ''
        elif node.node_type == 'Textarea':
            self.variables[node.name] = ''
        elif node.node_type == 'Checkbox':
            self.variables[node.name] = False
        elif node.node_type == 'Radio':
            self.variables[node.name] = ''
        elif node.node_type == 'Dropdown':
            self.variables[node.name] = ''
        elif node.node_type == 'Date':
            self.variables[node.name] = ''
        elif node.node_type == 'Time':
            self.variables[node.name] = ''
        elif node.node_type == 'Colour':
            self.variables[node.name] = '#000000'
        elif node.node_type == 'Slider':
            self.variables[node.name] = 50
        elif node.node_type == 'Upload':
            self.variables[node.name] = None
        elif node.node_type == 'MakeList':
            self.lists[node.name] = node.items or []
            self.variables[node.name] = self.lists[node.name]
        elif node.node_type == 'State':
            self.states[node.name] = node.initial_value
            self.variables[node.name] = node.initial_value
        elif node.node_type == 'Action':
            self.actions[node.name] = node
        elif node.node_type == 'Component':
            self.components[node.name] = node
        elif node.node_type == 'Assignment':
            if hasattr(node.value, 'value'):
                self.variables[node.variable] = node.value.value
        elif hasattr(node, 'children'):
            for child in node.children:
                self.collect_declarations(child)
    
    def generate_state_management(self):
        """Generate state management code"""
        if not self.states:
            return ''
        
        js = '\n// State Management\n'
        for name, value in self.states.items():
            js += f'let {name} = {json.dumps(value)};\n'
            # Generate setter function
            js += f'''function set{name.capitalize()}(newValue) {{
    {name} = newValue;
    // Trigger re-render for components using this state
    updateComponents();
}}
'''
        js += '\n'
        return js
    
    def generate_component_rendering(self, ast):
        """Generate component rendering code"""
        if not self.components:
            return ''
        
        js = '\n    // Component Rendering\n'
        for name, component in self.components.items():
            js += f'    function render{name}() {{\n'
            js += f'        const container = document.createElement("div");\n'
            js += f'        container.className = "nova-component-{name}";\n'
            # Render component body
            js += self.generate_component_body(component.body)
            js += f'        return container;\n'
            js += f'    }}\n'
        js += '\n    function updateComponents() {\n'
        for name in self.components:
            js += f'        const elements = document.querySelectorAll(".nova-component-{name}");\n'
            js += f'        elements.forEach(function(el) {{\n'
            js += f'            const newEl = render{name}();\n'
            js += f'            el.parentNode.replaceChild(newEl, el);\n'
            js += f'        }});\n'
        js += '    }\n\n'
        return js
    
    def generate_component_body(self, body):
        """Generate component body rendering"""
        js = ''
        for node in body:
            if node.node_type == 'Button':
                js += f'        const btn = document.createElement("button");\n'
                js += f'        btn.id = "{node.name}";\n'
                js += f'        btn.className = "nova-button";\n'
                js += f'        btn.textContent = "{node.text}";\n'
                js += f'        container.appendChild(btn);\n'
            elif node.node_type == 'Text':
                js += f'        const p = document.createElement("p");\n'
                js += f'        p.className = "nova-text";\n'
                js += f'        p.textContent = "{node.content}";\n'
                js += f'        container.appendChild(p);\n'
            elif node.node_type == 'Heading':
                js += f'        const h1 = document.createElement("h1");\n'
                js += f'        h1.className = "nova-heading";\n'
                js += f'        h1.textContent = "{node.content}";\n'
                js += f'        container.appendChild(h1);\n'
            # Add more component body rendering as needed
        return js
    
    def generate_node(self, node):
        if node.node_type == 'Page':
            for child in node.children:
                self.generate_node(child)
        
        elif node.node_type == 'When':
            self.generate_when(node)
        
        elif node.node_type == 'If':
            self.generate_if(node)
        
        elif node.node_type == 'Elif':
            # Handled inside if
            pass
        
        elif node.node_type == 'Otherwise':
            # Handled inside if
            pass
        
        elif node.node_type == 'Repeat':
            self.generate_repeat(node)
        
        elif node.node_type == 'RepeatWhile':
            self.generate_repeat_while(node)
        
        elif node.node_type == 'ForEach':
            self.generate_for_each(node)
        
        elif node.node_type == 'Stop':
            self.js += '        break;\n'
        
        elif node.node_type == 'Continue':
            self.js += '        continue;\n'
        
        elif node.node_type == 'Popup':
            self.generate_popup(node)
        
        elif node.node_type == 'Confirm':
            self.js += f'    confirm("{node.message}");\n'
        
        elif node.node_type == 'AskUser':
            self.js += f'    prompt("{node.message}");\n'
        
        elif node.node_type == 'Notification':
            self.js += f'    // Notification: {node.message}\n'
            self.js += f'    alert("{node.message}");\n'
        
        elif node.node_type == 'Toast':
            self.js += f'    // Toast: {node.message}\n'
            self.js += f'    console.log("Toast:", "{node.message}");\n'
        
        elif node.node_type == 'Progress':
            self.js += f'    // Progress: {node.value}%\n'
        
        elif node.node_type == 'Loading':
            self.js += f'    // Loading spinner\n'
        
        elif node.node_type == 'Assignment':
            self.generate_assignment(node)
        
        elif node.node_type == 'MakeList':
            self.js += f'    {node.name} = {json.dumps(node.items)};\n'
        
        elif node.node_type == 'AddItem':
            self.js += f'    {node.list_name}.push({self.get_value(node.item)});\n'
        
        elif node.node_type == 'RemoveItem':
            self.js += f'    {node.list_name}.splice({node.index}, 1);\n'
        
        elif node.node_type == 'InsertItem':
            self.js += f'    {node.list_name}.splice({node.index}, 0, {self.get_value(node.item)});\n'
        
        elif node.node_type == 'Sort':
            self.js += f'    {node.list_name}.sort();\n'
        
        elif node.node_type == 'Reverse':
            self.js += f'    {node.list_name}.reverse();\n'
        
        elif node.node_type == 'Shuffle':
            self.js += f'    {node.list_name} = shuffleArray({node.list_name});\n'
        
        elif node.node_type == 'ListLength':
            self.js += f'    // Length of {node.list_name}: {node.list_name}.length\n'
        
        elif node.node_type == 'ContainsItem':
            self.js += f'    // {node.list_name}.includes({self.get_value(node.item)})\n'
        
        elif node.node_type == 'Show':
            self.js += f'    document.getElementById("{node.element}").style.display = "block";\n'
        
        elif node.node_type == 'Hide':
            self.js += f'    document.getElementById("{node.element}").style.display = "none";\n'
        
        elif node.node_type == 'Enable':
            self.js += f'    document.getElementById("{node.element}").disabled = false;\n'
        
        elif node.node_type == 'Disable':
            self.js += f'    document.getElementById("{node.element}").disabled = true;\n'
        
        elif node.node_type == 'FadeIn':
            self.generate_fade_in(node)
        
        elif node.node_type == 'FadeOut':
            self.generate_fade_out(node)
        
        elif node.node_type == 'Slide':
            self.generate_slide(node)
        
        elif node.node_type == 'Grow':
            self.generate_grow(node)
        
        elif node.node_type == 'Shrink':
            self.generate_shrink(node)
        
        elif node.node_type == 'Rotate':
            self.generate_rotate(node)
        
        elif node.node_type == 'Bounce':
            self.generate_bounce(node)
        
        elif node.node_type == 'Spin':
            self.generate_spin(node)
        
        elif node.node_type == 'Shake':
            self.generate_shake(node)
        
        elif node.node_type == 'MoveTo':
            self.generate_moveto(node)
        
        elif node.node_type == 'MoveBy':
            self.generate_moveby(node)
        
        elif node.node_type == 'FlipHorizontal':
            self.js += f'    document.getElementById("{node.element}").style.transform = "scaleX(-1)";\n'
        
        elif node.node_type == 'FlipVertical':
            self.js += f'    document.getElementById("{node.element}").style.transform = "scaleY(-1)";\n'
        
        elif node.node_type == 'Animate':
            self.generate_animate(node)
        
        elif node.node_type == 'Run':
            self.js += f'    {node.name}({", ".join([json.dumps(arg) for arg in node.args])});\n'
        
        elif node.node_type == 'Return':
            self.js += f'    return {self.get_value(node.value)};\n'
        
        elif node.node_type == 'Use':
            self.js += f'    document.body.appendChild(render{node.name}());\n'
        
        elif node.node_type == 'State':
            # Already handled in collect_declarations
            pass
        
        elif node.node_type == 'ConnectDatabase':
            self.js += f'    // Connecting to database: {node.connection_string}\n'
        
        elif node.node_type == 'SaveDatabase':
            self.js += f'    // Saving to {node.collection}: {json.dumps(node.data)}\n'
        
        elif node.node_type == 'LoadDatabase':
            self.js += f'    // Loading from {node.collection}: {json.dumps(node.query)}\n'
        
        elif node.node_type == 'UpdateDatabase':
            self.js += f'    // Updating {node.collection}: {json.dumps(node.query)} -> {json.dumps(node.data)}\n'
        
        elif node.node_type == 'DeleteDatabase':
            self.js += f'    // Deleting from {node.collection}: {json.dumps(node.query)}\n'
        
        elif node.node_type == 'Login':
            self.js += f'    // Login: {node.username}\n'
        
        elif node.node_type == 'Logout':
            self.js += f'    // Logout\n'
        
        elif node.node_type == 'Signup':
            self.js += f'    // Signup: {node.username}, {node.email}\n'
        
        elif node.node_type == 'Encrypt':
            self.js += f'    // Encrypt: {node.data}\n'
            self.js += f'    const encrypted_{self.js.count("encrypted_")} = btoa("{node.data}");\n'
        
        elif node.node_type == 'Decrypt':
            self.js += f'    // Decrypt: {node.data}\n'
            self.js += f'    const decrypted_{self.js.count("decrypted_")} = atob("{node.data}");\n'
        
        elif node.node_type == 'Hash':
            self.js += f'    // Hash: {node.data}\n'
            self.js += f'    // Use crypto API for hashing\n'
        
        elif node.node_type == 'VerifyPassword':
            self.js += f'    // Verify password\n'
        
        elif node.node_type == 'GenerateToken':
            self.js += f'    // Generate token\n'
            self.js += f'    const token = Math.random().toString(36).substring(2);\n'
        
        elif node.node_type == 'SessionSave':
            self.js += f'    sessionStorage.setItem("{node.key}", {json.dumps(self.get_value(node.value))});\n'
        
        elif node.node_type == 'Cookie':
            self.js += f'    document.cookie = "{node.key}=" + {json.dumps(self.get_value(node.value))};\n'
        
        elif node.node_type == 'PutToServer':
            self.js += f'    // PUT request to {node.url}\n'
            self.js += f'    fetch("{node.url}", {{ method: "PUT", body: JSON.stringify({self.get_value(node.data)}) }});\n'
        
        elif node.node_type == 'DeleteFromServer':
            self.js += f'    // DELETE request to {node.url}\n'
            self.js += f'    fetch("{node.url}", {{ method: "DELETE" }});\n'
        
        elif node.node_type == 'Fetch':
            self.js += f'    // Fetch from {node.url}\n'
            self.js += f'    fetch("{node.url}")\n'
            self.js += f'        .then(response => response.json())\n'
            self.js += f'        .then(data => console.log(data));\n'
        
        elif node.node_type == 'SaveFile':
            self.js += f'    // Save file: {node.filename}\n'
            self.js += f'    const blob = new Blob([{self.get_value(node.content)}], {{ type: "text/plain" }});\n'
            self.js += f'    const link = document.createElement("a");\n'
            self.js += f'    link.href = URL.createObjectURL(blob);\n'
            self.js += f'    link.download = "{node.filename}";\n'
            self.js += f'    link.click();\n'
        
        elif node.node_type == 'OpenFile':
            self.js += f'    // Open file: {node.filename}\n'
            self.js += f'    const input = document.createElement("input");\n'
            self.js += f'    input.type = "file";\n'
            self.js += f'    input.accept = "{node.filename}";\n'
            self.js += f'    input.click();\n'
        
        elif node.node_type == 'DeleteFile':
            self.js += f'    // Delete file: {node.filename}\n'
        
        elif node.node_type == 'RenameFile':
            self.js += f'    // Rename file: {node.old_name} -> {node.new_name}\n'
        
        elif node.node_type == 'OpenWebsite':
            self.js += f'    window.open("{node.url}", "_blank");\n'
        
        elif node.node_type == 'SharePage':
            self.js += f'    if (navigator.share) {{ navigator.share({{ title: document.title, url: window.location.href }}); }}\n'
        
        elif node.node_type == 'CopyLink':
            self.js += f'    navigator.clipboard.writeText(window.location.href);\n'
        
        elif node.node_type == 'PrintPage':
            self.js += f'    window.print();\n'
        
        elif node.node_type == 'StopMedia':
            self.js += f'    const media_{self.js.count("media_")} = document.getElementById("{node.element}");\n'
            self.js += f'    if (media_{self.js.count("media_") - 1}) media_{self.js.count("media_") - 1}.stop();\n'
        
        elif node.node_type == 'Camera':
            self.js += f'    // Access camera\n'
            self.js += f'    navigator.mediaDevices.getUserMedia({{ video: true }});\n'
        
        elif node.node_type == 'TakePhoto':
            self.js += f'    // Take photo\n'
        
        elif node.node_type == 'RecordVideo':
            self.js += f'    // Record video\n'
        
        elif node.node_type == 'Microphone':
            self.js += f'    // Access microphone\n'
            self.js += f'    navigator.mediaDevices.getUserMedia({{ audio: true }});\n'
        
        elif node.node_type == 'RecordAudio':
            self.js += f'    // Record audio\n'
        
        elif node.node_type == 'Power':
            self.js += f'    Math.pow({node.base}, {node.exponent})\n'
        
        elif node.node_type == 'SquareRoot':
            self.js += f'    Math.sqrt({node.value})\n'
        
        elif node.node_type == 'Absolute':
            self.js += f'    Math.abs({node.value})\n'
        
        elif node.node_type == 'Floor':
            self.js += f'    Math.floor({node.value})\n'
        
        elif node.node_type == 'Ceiling':
            self.js += f'    Math.ceil({node.value})\n'
        
        elif node.node_type == 'Mod':
            self.js += f'    {self.get_value(node.left)} % {self.get_value(node.right)}\n'
        
        elif node.node_type == 'Uppercase':
            self.js += f'    "{node.value}".toUpperCase()\n'
        
        elif node.node_type == 'Lowercase':
            self.js += f'    "{node.value}".toLowerCase()\n'
        
        elif node.node_type == 'Capitalize':
            self.js += f'    "{node.value}".charAt(0).toUpperCase() + "{node.value}".slice(1).toLowerCase()\n'
        
        elif node.node_type == 'Trim':
            self.js += f'    "{node.value}".trim()\n'
        
        elif node.node_type == 'Replace':
            self.js += f'    "{node.string}".replace(/{node.old}/g, "{node.new}")\n'
        
        elif node.node_type == 'Contains':
            self.js += f'    "{node.string}".includes("{node.substring}")\n'
        
        elif node.node_type == 'StartsWith':
            self.js += f'    "{node.string}".startsWith("{node.prefix}")\n'
        
        elif node.node_type == 'EndsWith':
            self.js += f'    "{node.string}".endsWith("{node.suffix}")\n'
        
        elif node.node_type == 'LengthOf':
            self.js += f'    "{node.value}".length\n'
        
        elif hasattr(node, 'children'):
            for child in node.children:
                self.generate_node(child)
    
    def generate_when(self, when_node):
        element_id = when_node.element
        event = when_node.event
        actions = when_node.actions
        
        event_map = {
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
            'tapped': 'click',
            'doubletapped': 'dblclick',
            'longpressed': 'longpressed',
            'swipedleft': 'swipedleft',
            'swipedright': 'swipedright',
            'swipedup': 'swipedup',
            'swipeddown': 'swipeddown',
            'deviceshaken': 'deviceshaken',
            'devicetilted': 'devicetilted',
            'DOMContentLoaded': 'DOMContentLoaded',
            'beforeunload': 'beforeunload',
            'scroll': 'scroll'
        }
        
        js_event = event_map.get(event, event)
        
        if element_id == 'document':
            self.js += f'    document.addEventListener("{js_event}", function(e) {{\n'
        else:
            self.js += f'    document.getElementById("{element_id}").addEventListener("{js_event}", function(e) {{\n'
        
        # Special handling for keyboard events
        if event in ['enterpressed', 'escapepressed', 'spacepressed']:
            key_map = {
                'enterpressed': 'Enter',
                'escapepressed': 'Escape',
                'spacepressed': ' '
            }
            expected_key = key_map.get(event)
            self.js += f'        if (e.key !== "{expected_key}") return;\n'
        
        for action in actions:
            if action.node_type == 'Popup':
                self.js += f'        alert("{action.message}");\n'
            elif action.node_type == 'Assignment':
                self.js += f'        {action.variable} = {self.get_value(action.value)};\n'
            elif action.node_type == 'Show':
                self.js += f'        document.getElementById("{action.element}").style.display = "block";\n'
            elif action.node_type == 'Hide':
                self.js += f'        document.getElementById("{action.element}").style.display = "none";\n'
            elif action.node_type == 'Enable':
                self.js += f'        document.getElementById("{action.element}").disabled = false;\n'
            elif action.node_type == 'Disable':
                self.js += f'        document.getElementById("{action.element}").disabled = true;\n'
        
        self.js += '    });\n'
    
    def generate_if(self, if_node):
        condition = self.get_condition(if_node.condition)
        self.js += f'    if ({condition}) {{\n'
        
        for stmt in if_node.body:
            if stmt.node_type == 'Popup':
                self.js += f'        alert("{stmt.message}");\n'
            elif stmt.node_type == 'Assignment':
                self.js += f'        {stmt.variable} = {self.get_value(stmt.value)};\n'
            elif stmt.node_type == 'Show':
                self.js += f'        document.getElementById("{stmt.element}").style.display = "block";\n'
            elif stmt.node_type == 'Hide':
                self.js += f'        document.getElementById("{stmt.element}").style.display = "none";\n'
        
        self.js += '    }\n'
        
        # Handle elif conditions
        if hasattr(if_node, 'elif_conditions') and if_node.elif_conditions:
            for elif_cond in if_node.elif_conditions:
                self.js += f'    else if ({self.get_condition(elif_cond.condition)}) {{\n'
                for stmt in elif_cond.body:
                    if stmt.node_type == 'Popup':
                        self.js += f'        alert("{stmt.message}");\n'
                    elif stmt.node_type == 'Assignment':
                        self.js += f'        {stmt.variable} = {self.get_value(stmt.value)};\n'
                self.js += '    }\n'
        
        if hasattr(if_node, 'else_body') and if_node.else_body:
            self.js += '    else {\n'
            for stmt in if_node.else_body:
                if stmt.node_type == 'Popup':
                    self.js += f'        alert("{stmt.message}");\n'
            self.js += '    }\n'
    
    def generate_repeat(self, repeat_node):
        self.js += f'    for (let i = 0; i < {repeat_node.count}; i++) {{\n'
        for stmt in repeat_node.body:
            if stmt.node_type == 'Popup':
                self.js += f'        alert("{stmt.message}");\n'
            elif stmt.node_type == 'Text':
                self.js += f'        console.log("{stmt.content}");\n'
            elif stmt.node_type == 'Assignment':
                self.js += f'        {stmt.variable} = {self.get_value(stmt.value)};\n'
        self.js += '    }\n'
    
    def generate_repeat_while(self, repeat_while_node):
        condition = self.get_condition(repeat_while_node.condition)
        self.js += f'    while ({condition}) {{\n'
        for stmt in repeat_while_node.body:
            if stmt.node_type == 'Popup':
                self.js += f'        alert("{stmt.message}");\n'
            elif stmt.node_type == 'Text':
                self.js += f'        console.log("{stmt.content}");\n'
            elif stmt.node_type == 'Assignment':
                self.js += f'        {stmt.variable} = {self.get_value(stmt.value)};\n'
        self.js += '    }\n'
    
    def generate_for_each(self, for_each_node):
        self.js += f'    for (let {for_each_node.item} of {for_each_node.list_name}) {{\n'
        for stmt in for_each_node.body:
            if stmt.node_type == 'Popup':
                self.js += f'        alert("{stmt.message}");\n'
            elif stmt.node_type == 'Text':
                self.js += f'        console.log({for_each_node.item});\n'
        self.js += '    }\n'
    
    def generate_fade_in(self, fade_in_node):
        self.js += f'''    const el_{self.js.count("el_")} = document.getElementById("{fade_in_node.element}");
    if (el_{self.js.count("el_") - 1}) {{
        el_{self.js.count("el_") - 1}.style.transition = "opacity {fade_in_node.duration}ms";
        el_{self.js.count("el_") - 1}.style.opacity = "1";
    }}
'''
    
    def generate_fade_out(self, fade_out_node):
        self.js += f'''    const el_{self.js.count("el_")} = document.getElementById("{fade_out_node.element}");
    if (el_{self.js.count("el_") - 1}) {{
        el_{self.js.count("el_") - 1}.style.transition = "opacity {fade_out_node.duration}ms";
        el_{self.js.count("el_") - 1}.style.opacity = "0";
    }}
'''
    
    def generate_slide(self, slide_node):
        direction_map = {
            'left': 'translateX(-100px)',
            'right': 'translateX(100px)',
            'up': 'translateY(-100px)',
            'down': 'translateY(100px)'
        }
        transform = direction_map.get(slide_node.direction, 'translateX(-100px)')
        self.js += f'''    const el_{self.js.count("el_")} = document.getElementById("{slide_node.element}");
    if (el_{self.js.count("el_") - 1}) {{
        el_{self.js.count("el_") - 1}.style.transition = "transform 300ms";
        el_{self.js.count("el_") - 1}.style.transform = "{transform}";
        setTimeout(() => {{
            el_{self.js.count("el_") - 1}.style.transform = "translate(0)";
        }}, 300);
    }}
'''
    
    def generate_grow(self, grow_node):
        self.js += f'''    const el_{self.js.count("el_")} = document.getElementById("{grow_node.element}");
    if (el_{self.js.count("el_") - 1}) {{
        el_{self.js.count("el_") - 1}.style.transition = "transform 300ms";
        el_{self.js.count("el_") - 1}.style.transform = "scale({grow_node.scale})";
        setTimeout(() => {{
            el_{self.js.count("el_") - 1}.style.transform = "scale(1)";
        }}, 300);
    }}
'''
    
    def generate_shrink(self, shrink_node):
        self.js += f'''    const el_{self.js.count("el_")} = document.getElementById("{shrink_node.element}");
    if (el_{self.js.count("el_") - 1}) {{
        el_{self.js.count("el_") - 1}.style.transition = "transform 300ms";
        el_{self.js.count("el_") - 1}.style.transform = "scale({shrink_node.scale})";
        setTimeout(() => {{
            el_{self.js.count("el_") - 1}.style.transform = "scale(1)";
        }}, 300);
    }}
'''
    
    def generate_rotate(self, rotate_node):
        self.js += f'''    const el_{self.js.count("el_")} = document.getElementById("{rotate_node.element}");
    if (el_{self.js.count("el_") - 1}) {{
        el_{self.js.count("el_") - 1}.style.transition = "transform 300ms";
        el_{self.js.count("el_") - 1}.style.transform = "rotate({rotate_node.degrees}deg)";
    }}
'''
    
    def generate_bounce(self, bounce_node):
        self.js += f'''    const el_{self.js.count("el_")} = document.getElementById("{bounce_node.element}");
    if (el_{self.js.count("el_") - 1}) {{
        el_{self.js.count("el_") - 1}.style.animation = "bounce 0.5s ease";
        el_{self.js.count("el_") - 1}.addEventListener("animationend", function() {{
            this.style.animation = "";
        }});
    }}
'''
    
    def generate_spin(self, spin_node):
        self.js += f'''    const el_{self.js.count("el_")} = document.getElementById("{spin_node.element}");
    if (el_{self.js.count("el_") - 1}) {{
        el_{self.js.count("el_") - 1}.style.animation = "spin 1s linear infinite";
    }}
'''
    
    def generate_shake(self, shake_node):
        self.js += f'''    const el_{self.js.count("el_")} = document.getElementById("{shake_node.element}");
    if (el_{self.js.count("el_") - 1}) {{
        el_{self.js.count("el_") - 1}.style.animation = "shake 0.5s ease";
        el_{self.js.count("el_") - 1}.addEventListener("animationend", function() {{
            this.style.animation = "";
        }});
    }}
'''
    
    def generate_moveto(self, moveto_node):
        self.js += f'''    const el_{self.js.count("el_")} = document.getElementById("{moveto_node.element}");
    if (el_{self.js.count("el_") - 1}) {{
        el_{self.js.count("el_") - 1}.style.transition = "all 300ms";
        el_{self.js.count("el_") - 1}.style.position = "absolute";
        el_{self.js.count("el_") - 1}.style.left = "{moveto_node.x}px";
        el_{self.js.count("el_") - 1}.style.top = "{moveto_node.y}px";
    }}
'''
    
    def generate_moveby(self, moveby_node):
        self.js += f'''    const el_{self.js.count("el_")} = document.getElementById("{moveby_node.element}");
    if (el_{self.js.count("el_") - 1}) {{
        const rect = el_{self.js.count("el_") - 1}.getBoundingClientRect();
        el_{self.js.count("el_") - 1}.style.transition = "all 300ms";
        el_{self.js.count("el_") - 1}.style.position = "absolute";
        el_{self.js.count("el_") - 1}.style.left = (rect.left + {moveby_node.dx}) + "px";
        el_{self.js.count("el_") - 1}.style.top = (rect.top + {moveby_node.dy}) + "px";
    }}
'''
    
    def generate_animate(self, animate_node):
        self.js += f'''    const el_{self.js.count("el_")} = document.getElementById("{animate_node.element}");
    if (el_{self.js.count("el_") - 1}) {{
        el_{self.js.count("el_") - 1}.style.animation = "{animate_node.animation} {animate_node.duration}ms";
        el_{self.js.count("el_") - 1}.addEventListener("animationend", function() {{
            this.style.animation = "";
        }});
    }}
'''
    
    def generate_actions(self):
        """Generate action functions"""
        js = '\n// Actions/Functions\n'
        for name, action in self.actions.items():
            params_str = ', '.join(action.params) if action.params else ''
            js += f'function {name}({params_str}) {{\n'
            for stmt in action.body:
                if stmt.node_type == 'Popup':
                    js += f'    alert("{stmt.message}");\n'
                elif stmt.node_type == 'Assignment':
                    js += f'    {stmt.variable} = {self.get_value(stmt.value)};\n'
                elif stmt.node_type == 'Return':
                    js += f'    return {self.get_value(stmt.value)};\n'
            js += '}\n\n'
        return js
    
    def get_value(self, value_node):
        if hasattr(value_node, 'value'):
            if hasattr(value_node.value, 'value'):
                return value_node.value.value
            return value_node.value
        return value_node
    
    def get_condition(self, condition):
        if hasattr(condition, 'left') and hasattr(condition, 'right'):
            left = self.get_value(condition.left)
            right = self.get_value(condition.right)
            op = condition.operator
            
            # Handle logical operators
            if op == 'and':
                return f'{left} && {right}'
            elif op == 'or':
                return f'{left} || {right}'
            elif op == 'not':
                return f'!{left}'
            
            return f'{left} {op} {right}'
        return str(condition)
    
    def generate_slideshow_js(self, ast):
        """Generate JavaScript for slideshow functionality"""
        js = ''
        has_slideshow = False
        
        def check_slideshow(node):
            nonlocal has_slideshow
            if node.node_type == 'Slideshow':
                has_slideshow = True
            elif hasattr(node, 'children'):
                for child in node.children:
                    check_slideshow(child)
        
        for node in ast:
            check_slideshow(node)
        
        if has_slideshow:
            js += '''
    // Slideshow functionality
    const slideshows = document.querySelectorAll('.nova-slideshow');
    slideshows.forEach(function(slideshow) {
        const slides = slideshow.querySelectorAll('.nova-slide');
        let currentSlide = 0;
        
        function showSlide(index) {
            slides.forEach(function(slide, i) {
                slide.style.display = i === index ? 'block' : 'none';
            });
        }
        
        const controls = slideshow.parentElement.querySelector('.nova-slideshow-controls');
        if (controls) {
            const prevBtn = controls.querySelector('.nova-slideshow-prev');
            const nextBtn = controls.querySelector('.nova-slideshow-next');
            
            if (prevBtn) {
                prevBtn.addEventListener('click', function() {
                    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
                    showSlide(currentSlide);
                });
            }
            
            if (nextBtn) {
                nextBtn.addEventListener('click', function() {
                    currentSlide = (currentSlide + 1) % slides.length;
                    showSlide(currentSlide);
                });
            }
        }
        
        setInterval(function() {
            currentSlide = (currentSlide + 1) % slides.length;
            showSlide(currentSlide);
        }, 3000);
    });
'''
        return js
    
    def generate_tabs_js(self, ast):
        """Generate JavaScript for tabs functionality"""
        js = ''
        has_tabs = False
        
        def check_tabs(node):
            nonlocal has_tabs
            if node.node_type == 'Tabs':
                has_tabs = True
            elif hasattr(node, 'children'):
                for child in node.children:
                    check_tabs(child)
        
        for node in ast:
            check_tabs(node)
        
        if has_tabs:
            js += '''
    // Tabs functionality
    document.querySelectorAll('.nova-tabs').forEach(function(tabsContainer) {
        const buttons = tabsContainer.querySelectorAll('.nova-tab-btn');
        const contents = tabsContainer.querySelectorAll('.nova-tab-content');
        
        buttons.forEach(function(button) {
            button.addEventListener('click', function() {
                buttons.forEach(function(btn) {
                    btn.classList.remove('active');
                });
                button.classList.add('active');
                
                contents.forEach(function(content) {
                    content.style.display = 'none';
                });
                
                const tabIndex = button.getAttribute('data-tab');
                const targetContent = tabsContainer.querySelector('.nova-tab-content[data-tab="' + tabIndex + '"]');
                if (targetContent) {
                    targetContent.style.display = 'block';
                }
            });
        });
    });
'''
        return js
    
    def generate_event_handlers(self, ast):
        """Generate JavaScript for event handlers"""
        js = ''
        
        def collect_events(nodes):
            events = []
            for node in nodes:
                if node.node_type == 'When':
                    events.append(node)
                elif hasattr(node, 'children'):
                    events.extend(collect_events(node.children))
            return events
        
        all_events = collect_events(ast)
        
        event_map = {
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
            'blur': 'blur'
        }
        
        for event in all_events:
            if event.element == 'document':
                js += f'    document.addEventListener("{event_map.get(event.event, event.event)}", function(e) {{\n'
            else:
                js += f'    document.getElementById("{event.element}").addEventListener("{event_map.get(event.event, event.event)}", function(e) {{\n'
            
            if event.event in ['enterpressed', 'escapepressed', 'spacepressed']:
                key_map = {
                    'enterpressed': 'Enter',
                    'escapepressed': 'Escape',
                    'spacepressed': ' '
                }
                expected_key = key_map.get(event.event)
                js += f'        if (e.key !== "{expected_key}") return;\n'
            
            for action in event.actions:
                if action.node_type == 'Popup':
                    js += f'        alert("{action.message}");\n'
                elif action.node_type == 'Assignment':
                    js += f'        {action.variable} = {self.get_value(action.value)};\n'
            
            js += '    });\n'
        
        return js
    
    def generate_mouse_js(self, ast):
        """Generate JavaScript for mouse tracking"""
        js = ''
        has_mouse = False
        
        def check_mouse(node):
            nonlocal has_mouse
            if node.node_type == 'When' and node.event in ['mousemoves', 'mousewheel']:
                has_mouse = True
            elif hasattr(node, 'children'):
                for child in node.children:
                    check_mouse(child)
        
        for node in ast:
            check_mouse(node)
        
        if has_mouse:
            js += '''
    // Mouse tracking
    let mouseX = 0;
    let mouseY = 0;
    
    document.addEventListener('mousemove', function(e) {
        mouseX = e.clientX;
        mouseY = e.clientY;
        document.dispatchEvent(new CustomEvent('mousemoves', { 
            detail: { x: e.clientX, y: e.clientY } 
        }));
    });
    
    document.addEventListener('wheel', function(e) {
        document.dispatchEvent(new CustomEvent('mousewheel', { 
            detail: { deltaX: e.deltaX, deltaY: e.deltaY, deltaZ: e.deltaZ } 
        }));
    });
'''
        return js
    
    def generate_keyboard_js(self, ast):
        """Generate JavaScript for keyboard tracking"""
        js = ''
        has_keyboard = False
        
        def check_keyboard(node):
            nonlocal has_keyboard
            if node.node_type == 'When' and node.event in ['keypressed', 'keyreleased', 'enterpressed', 'escapepressed', 'spacepressed']:
                has_keyboard = True
            elif hasattr(node, 'children'):
                for child in node.children:
                    check_keyboard(child)
        
        for node in ast:
            check_keyboard(node)
        
        if has_keyboard:
            js += '''
    // Keyboard tracking
    let shiftPressed = false;
    let controlPressed = false;
    let altPressed = false;
    let lastKey = '';
    
    document.addEventListener('keydown', function(e) {
        shiftPressed = e.shiftKey;
        controlPressed = e.ctrlKey;
        altPressed = e.altKey;
        lastKey = e.key;
        
        if (e.key === 'Enter') {
            document.dispatchEvent(new CustomEvent('enterpressed', { detail: { key: e.key } }));
        }
        if (e.key === 'Escape') {
            document.dispatchEvent(new CustomEvent('escapepressed', { detail: { key: e.key } }));
        }
        if (e.key === ' ') {
            document.dispatchEvent(new CustomEvent('spacepressed', { detail: { key: e.key } }));
        }
        document.dispatchEvent(new CustomEvent('keypressed', { detail: { key: e.key, shift: e.shiftKey, ctrl: e.ctrlKey, alt: e.altKey } }));
    });
    
    document.addEventListener('keyup', function(e) {
        shiftPressed = e.shiftKey;
        controlPressed = e.ctrlKey;
        altPressed = e.altKey;
        document.dispatchEvent(new CustomEvent('keyreleased', { detail: { key: e.key, shift: e.shiftKey, ctrl: e.ctrlKey, alt: e.altKey } }));
    });
'''
        return js
    
    def generate_touch_js(self, ast):
        """Generate JavaScript for touch tracking"""
        js = ''
        has_touch = False
        
        def check_touch(node):
            nonlocal has_touch
            if node.node_type == 'When' and node.event in ['tapped', 'doubletapped', 'longpressed', 'swipedleft', 'swipedright', 'swipedup', 'swipeddown']:
                has_touch = True
            elif hasattr(node, 'children'):
                for child in node.children:
                    check_touch(child)
        
        for node in ast:
            check_touch(node)
        
        if has_touch:
            js += '''
    // Touch tracking
    let touchStartX = 0;
    let touchStartY = 0;
    let touchStartTime = 0;
    let lastTapTime = 0;
    let longPressTimer = null;
    
    document.addEventListener('touchstart', function(e) {
        const touch = e.touches[0];
        touchStartX = touch.clientX;
        touchStartY = touch.clientY;
        touchStartTime = Date.now();
        
        longPressTimer = setTimeout(function() {
            document.dispatchEvent(new CustomEvent('longpressed', { 
                detail: { x: touch.clientX, y: touch.clientY } 
            }));
        }, 500);
    });
    
    document.addEventListener('touchmove', function(e) {
        clearTimeout(longPressTimer);
    });
    
    document.addEventListener('touchend', function(e) {
        clearTimeout(longPressTimer);
        
        const touchEndX = e.changedTouches[0].clientX;
        const touchEndY = e.changedTouches[0].clientY;
        const touchEndTime = Date.now();
        
        const dx = touchEndX - touchStartX;
        const dy = touchEndY - touchStartY;
        const distance = Math.sqrt(dx * dx + dy * dy);
        const timeDiff = touchEndTime - touchStartTime;
        
        if (distance < 30 && timeDiff < 300) {
            const now = Date.now();
            if (now - lastTapTime < 300) {
                document.dispatchEvent(new CustomEvent('doubletapped', { 
                    detail: { x: touchEndX, y: touchEndY } 
                }));
                lastTapTime = 0;
            } else {
                document.dispatchEvent(new CustomEvent('tapped', { 
                    detail: { x: touchEndX, y: touchEndY } 
                }));
                lastTapTime = now;
            }
        }
        
        if (distance > 50) {
            if (Math.abs(dx) > Math.abs(dy)) {
                if (dx > 0) {
                    document.dispatchEvent(new CustomEvent('swipedright', { 
                        detail: { dx: dx, dy: dy } 
                    }));
                } else {
                    document.dispatchEvent(new CustomEvent('swipedleft', { 
                        detail: { dx: dx, dy: dy } 
                    }));
                }
            } else {
                if (dy > 0) {
                    document.dispatchEvent(new CustomEvent('swipeddown', { 
                        detail: { dx: dx, dy: dy } 
                    }));
                } else {
                    document.dispatchEvent(new CustomEvent('swipedup', { 
                        detail: { dx: dx, dy: dy } 
                    }));
                }
            }
        }
    });
'''
        return js
    
    def generate_device_js(self, ast):
        """Generate JavaScript for device events"""
        js = ''
        has_device = False
        
        def check_device(node):
            nonlocal has_device
            if node.node_type == 'When' and node.event in ['deviceshaken', 'devicetilted']:
                has_device = True
            elif hasattr(node, 'children'):
                for child in node.children:
                    check_device(child)
        
        for node in ast:
            check_device(node)
        
        if has_device:
            js += '''
    // Device events
    if (window.DeviceOrientationEvent) {
        window.addEventListener('deviceorientation', function(e) {
            document.dispatchEvent(new CustomEvent('devicetilted', { 
                detail: { 
                    alpha: e.alpha, 
                    beta: e.beta, 
                    gamma: e.gamma 
                } 
            }));
        });
    }
    
    if (window.DeviceMotionEvent) {
        let lastShakeTime = 0;
        window.addEventListener('devicemotion', function(e) {
            const acceleration = e.acceleration;
            const total = Math.sqrt(
                (acceleration.x || 0) ** 2 + 
                (acceleration.y || 0) ** 2 + 
                (acceleration.z || 0) ** 2
            );
            
            if (total > 20) {
                const now = Date.now();
                if (now - lastShakeTime > 500) {
                    document.dispatchEvent(new CustomEvent('deviceshaken', { 
                        detail: { 
                            x: acceleration.x, 
                            y: acceleration.y, 
                            z: acceleration.z 
                        } 
                    }));
                    lastShakeTime = now;
                }
            }
        });
    }
'''
        return js