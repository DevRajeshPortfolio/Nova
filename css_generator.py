# css_generator.py
# Nova Programming Language - CSS Generator

class CSSGenerator:
    def __init__(self):
        self.css = ''
    
    def generate(self, ast):
        """Generate CSS from AST"""
        self.css = '/* Nova Generated CSS */\n\n'
        self.css += 'body {\n'
        self.css += '    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;\n'
        self.css += '    margin: 0;\n'
        self.css += '    padding: 20px;\n'
        self.css += '    line-height: 1.6;\n'
        self.css += '    color: #333;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-container {\n'
        self.css += '    max-width: 1200px;\n'
        self.css += '    margin: 0 auto;\n'
        self.css += '    padding: 20px;\n'
        self.css += '}\n\n'
        
        # Buttons
        self.css += '.nova-button {\n'
        self.css += '    background-color: #007bff;\n'
        self.css += '    color: white;\n'
        self.css += '    border: none;\n'
        self.css += '    padding: 10px 20px;\n'
        self.css += '    border-radius: 5px;\n'
        self.css += '    cursor: pointer;\n'
        self.css += '    font-size: 16px;\n'
        self.css += '    margin: 5px;\n'
        self.css += '    transition: all 0.3s ease;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-button:hover {\n'
        self.css += '    background-color: #0056b3;\n'
        self.css += '}\n\n'
        
        # Inputs
        self.css += '.nova-input-group {\n'
        self.css += '    margin: 10px 0;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-input {\n'
        self.css += '    padding: 8px 12px;\n'
        self.css += '    border: 1px solid #ddd;\n'
        self.css += '    border-radius: 4px;\n'
        self.css += '    font-size: 16px;\n'
        self.css += '    width: 100%;\n'
        self.css += '    max-width: 300px;\n'
        self.css += '    margin: 5px 0;\n'
        self.css += '    box-sizing: border-box;\n'
        self.css += '    transition: border-color 0.3s ease, box-shadow 0.3s ease;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-input:focus {\n'
        self.css += '    outline: none;\n'
        self.css += '    border-color: #007bff;\n'
        self.css += '    box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);\n'
        self.css += '}\n\n'
        
        self.css += '.nova-label {\n'
        self.css += '    display: block;\n'
        self.css += '    margin: 5px 0;\n'
        self.css += '    font-weight: 500;\n'
        self.css += '}\n\n'
        
        # Text elements
        self.css += '.nova-text {\n'
        self.css += '    margin: 10px 0;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-heading {\n'
        self.css += '    margin: 20px 0 10px 0;\n'
        self.css += '    font-size: 2.5em;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-subtitle {\n'
        self.css += '    margin: 15px 0 10px 0;\n'
        self.css += '    font-size: 1.8em;\n'
        self.css += '    color: #555;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-small {\n'
        self.css += '    font-size: 0.8em;\n'
        self.css += '    color: #666;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-quote {\n'
        self.css += '    padding: 10px 20px;\n'
        self.css += '    margin: 10px 0;\n'
        self.css += '    border-left: 4px solid #007bff;\n'
        self.css += '    background-color: #f8f9fa;\n'
        self.css += '    font-style: italic;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-code {\n'
        self.css += '    font-family: "Courier New", monospace;\n'
        self.css += '    background-color: #f4f4f4;\n'
        self.css += '    padding: 2px 6px;\n'
        self.css += '    border-radius: 3px;\n'
        self.css += '    font-size: 0.9em;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-link {\n'
        self.css += '    color: #007bff;\n'
        self.css += '    text-decoration: none;\n'
        self.css += '    transition: color 0.3s ease;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-link:hover {\n'
        self.css += '    text-decoration: underline;\n'
        self.css += '}\n\n'
        
        # Checkbox and Radio
        self.css += '.nova-checkbox-group,\n'
        self.css += '.nova-radio-group {\n'
        self.css += '    margin: 10px 0;\n'
        self.css += '    display: flex;\n'
        self.css += '    align-items: center;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-checkbox-group input,\n'
        self.css += '.nova-radio-group input {\n'
        self.css += '    margin-right: 8px;\n'
        self.css += '    width: 18px;\n'
        self.css += '    height: 18px;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-checkbox-group .nova-label,\n'
        self.css += '.nova-radio-group .nova-label {\n'
        self.css += '    margin: 0;\n'
        self.css += '}\n\n'
        
        # Dropdown
        self.css += '.nova-dropdown {\n'
        self.css += '    padding: 8px 12px;\n'
        self.css += '    border: 1px solid #ddd;\n'
        self.css += '    border-radius: 4px;\n'
        self.css += '    font-size: 16px;\n'
        self.css += '    width: 100%;\n'
        self.css += '    max-width: 300px;\n'
        self.css += '    margin: 5px 0;\n'
        self.css += '    background-color: white;\n'
        self.css += '    transition: border-color 0.3s ease;\n'
        self.css += '}\n\n'
        
        # Textarea
        self.css += '.nova-textarea {\n'
        self.css += '    padding: 8px 12px;\n'
        self.css += '    border: 1px solid #ddd;\n'
        self.css += '    border-radius: 4px;\n'
        self.css += '    font-size: 16px;\n'
        self.css += '    width: 100%;\n'
        self.css += '    max-width: 500px;\n'
        self.css += '    margin: 5px 0;\n'
        self.css += '    box-sizing: border-box;\n'
        self.css += '    font-family: inherit;\n'
        self.css += '    transition: border-color 0.3s ease, box-shadow 0.3s ease;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-textarea:focus {\n'
        self.css += '    outline: none;\n'
        self.css += '    border-color: #007bff;\n'
        self.css += '    box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);\n'
        self.css += '}\n\n'
        
        # Slider
        self.css += '.nova-slider {\n'
        self.css += '    width: 100%;\n'
        self.css += '    max-width: 300px;\n'
        self.css += '    margin: 5px 0;\n'
        self.css += '}\n\n'
        
        # Colour picker
        self.css += '.nova-colour {\n'
        self.css += '    width: 60px;\n'
        self.css += '    height: 40px;\n'
        self.css += '    padding: 2px;\n'
        self.css += '    border: 1px solid #ddd;\n'
        self.css += '    border-radius: 4px;\n'
        self.css += '    cursor: pointer;\n'
        self.css += '}\n\n'
        
        # Upload
        self.css += '.nova-upload {\n'
        self.css += '    padding: 8px 12px;\n'
        self.css += '    border: 2px dashed #ddd;\n'
        self.css += '    border-radius: 4px;\n'
        self.css += '    width: 100%;\n'
        self.css += '    max-width: 300px;\n'
        self.css += '    margin: 5px 0;\n'
        self.css += '    box-sizing: border-box;\n'
        self.css += '    transition: border-color 0.3s ease;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-upload:hover {\n'
        self.css += '    border-color: #007bff;\n'
        self.css += '}\n\n'
        
        # Result
        self.css += '.nova-result {\n'
        self.css += '    margin: 20px 0;\n'
        self.css += '    padding: 15px;\n'
        self.css += '    background-color: #f8f9fa;\n'
        self.css += '    border-radius: 5px;\n'
        self.css += '    border: 1px solid #e9ecef;\n'
        self.css += '    font-size: 18px;\n'
        self.css += '    font-weight: 500;\n'
        self.css += '}\n\n'
        
        # NEW CSS STYLES
        
        # Image
        self.css += '.nova-image {\n'
        self.css += '    max-width: 100%;\n'
        self.css += '    height: auto;\n'
        self.css += '    border-radius: 4px;\n'
        self.css += '}\n\n'
        
        # Video
        self.css += '.nova-video {\n'
        self.css += '    max-width: 100%;\n'
        self.css += '    border-radius: 4px;\n'
        self.css += '}\n\n'
        
        # Audio
        self.css += '.nova-audio {\n'
        self.css += '    width: 100%;\n'
        self.css += '    max-width: 400px;\n'
        self.css += '}\n\n'
        
        # Gallery
        self.css += '.nova-gallery {\n'
        self.css += '    display: grid;\n'
        self.css += '    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));\n'
        self.css += '    gap: 10px;\n'
        self.css += '    margin: 10px 0;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-gallery-image {\n'
        self.css += '    width: 100%;\n'
        self.css += '    height: 150px;\n'
        self.css += '    object-fit: cover;\n'
        self.css += '    border-radius: 4px;\n'
        self.css += '}\n\n'
        
        # Slideshow
        self.css += '.nova-slideshow {\n'
        self.css += '    position: relative;\n'
        self.css += '    width: 100%;\n'
        self.css += '    max-width: 800px;\n'
        self.css += '    margin: 10px auto;\n'
        self.css += '    overflow: hidden;\n'
        self.css += '    border-radius: 4px;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-slide {\n'
        self.css += '    width: 100%;\n'
        self.css += '    height: 400px;\n'
        self.css += '    object-fit: cover;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-slideshow-controls {\n'
        self.css += '    display: flex;\n'
        self.css += '    justify-content: center;\n'
        self.css += '    gap: 10px;\n'
        self.css += '    margin: 10px 0;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-slideshow-controls button {\n'
        self.css += '    background-color: #007bff;\n'
        self.css += '    color: white;\n'
        self.css += '    border: none;\n'
        self.css += '    padding: 10px 20px;\n'
        self.css += '    border-radius: 5px;\n'
        self.css += '    cursor: pointer;\n'
        self.css += '    font-size: 16px;\n'
        self.css += '    transition: background-color 0.3s ease;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-slideshow-controls button:hover {\n'
        self.css += '    background-color: #0056b3;\n'
        self.css += '}\n\n'
        
        # Card
        self.css += '.nova-card {\n'
        self.css += '    background: white;\n'
        self.css += '    border-radius: 8px;\n'
        self.css += '    box-shadow: 0 2px 8px rgba(0,0,0,0.1);\n'
        self.css += '    padding: 20px;\n'
        self.css += '    margin: 10px 0;\n'
        self.css += '    transition: box-shadow 0.3s ease;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-card:hover {\n'
        self.css += '    box-shadow: 0 4px 16px rgba(0,0,0,0.15);\n'
        self.css += '}\n\n'
        
        self.css += '.nova-card-title {\n'
        self.css += '    margin: 0 0 10px 0;\n'
        self.css += '    font-size: 1.2em;\n'
        self.css += '}\n\n'
        
        # Section
        self.css += '.nova-section {\n'
        self.css += '    margin: 20px 0;\n'
        self.css += '    padding: 20px;\n'
        self.css += '    background: #f8f9fa;\n'
        self.css += '    border-radius: 8px;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-section-title {\n'
        self.css += '    margin: 0 0 15px 0;\n'
        self.css += '    font-size: 1.5em;\n'
        self.css += '}\n\n'
        
        # Navbar
        self.css += '.nova-navbar {\n'
        self.css += '    background: #333;\n'
        self.css += '    color: white;\n'
        self.css += '    padding: 10px 20px;\n'
        self.css += '    border-radius: 4px;\n'
        self.css += '    margin: 10px 0;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-navbar-list {\n'
        self.css += '    list-style: none;\n'
        self.css += '    margin: 0;\n'
        self.css += '    padding: 0;\n'
        self.css += '    display: flex;\n'
        self.css += '    gap: 20px;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-nav-link {\n'
        self.css += '    color: white;\n'
        self.css += '    text-decoration: none;\n'
        self.css += '    padding: 5px 10px;\n'
        self.css += '    border-radius: 4px;\n'
        self.css += '    transition: background-color 0.3s ease;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-nav-link:hover {\n'
        self.css += '    background: #555;\n'
        self.css += '}\n\n'
        
        # Footer
        self.css += '.nova-footer {\n'
        self.css += '    background: #333;\n'
        self.css += '    color: white;\n'
        self.css += '    padding: 20px;\n'
        self.css += '    border-radius: 4px;\n'
        self.css += '    margin: 20px 0;\n'
        self.css += '    text-align: center;\n'
        self.css += '}\n\n'
        
        # Sidebar
        self.css += '.nova-sidebar {\n'
        self.css += '    background: #f8f9fa;\n'
        self.css += '    padding: 20px;\n'
        self.css += '    border-radius: 8px;\n'
        self.css += '    margin: 10px 0;\n'
        self.css += '}\n\n'
        
        # Row
        self.css += '.nova-row {\n'
        self.css += '    display: flex;\n'
        self.css += '    flex-direction: row;\n'
        self.css += '    gap: 20px;\n'
        self.css += '    flex-wrap: wrap;\n'
        self.css += '    margin: 10px 0;\n'
        self.css += '}\n\n'
        
        # Column
        self.css += '.nova-column {\n'
        self.css += '    display: flex;\n'
        self.css += '    flex-direction: column;\n'
        self.css += '    gap: 10px;\n'
        self.css += '    flex: 1;\n'
        self.css += '    min-width: 200px;\n'
        self.css += '}\n\n'
        
        # Grid
        self.css += '.nova-grid {\n'
        self.css += '    display: grid;\n'
        self.css += '    gap: 20px;\n'
        self.css += '    margin: 10px 0;\n'
        self.css += '}\n\n'
        
        # Tabs
        self.css += '.nova-tabs {\n'
        self.css += '    margin: 10px 0;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-tab-headers {\n'
        self.css += '    display: flex;\n'
        self.css += '    gap: 5px;\n'
        self.css += '    border-bottom: 2px solid #ddd;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-tab-btn {\n'
        self.css += '    padding: 10px 20px;\n'
        self.css += '    border: none;\n'
        self.css += '    background: none;\n'
        self.css += '    cursor: pointer;\n'
        self.css += '    font-size: 16px;\n'
        self.css += '    border-bottom: 2px solid transparent;\n'
        self.css += '    margin-bottom: -2px;\n'
        self.css += '    transition: all 0.3s ease;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-tab-btn.active {\n'
        self.css += '    border-bottom-color: #007bff;\n'
        self.css += '    color: #007bff;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-tab-btn:hover {\n'
        self.css += '    background: #f8f9fa;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-tab-content {\n'
        self.css += '    padding: 20px;\n'
        self.css += '    border: 1px solid #ddd;\n'
        self.css += '    border-top: none;\n'
        self.css += '    border-radius: 0 0 4px 4px;\n'
        self.css += '}\n\n'
        
        # Panel
        self.css += '.nova-panel {\n'
        self.css += '    background: white;\n'
        self.css += '    border: 1px solid #ddd;\n'
        self.css += '    border-radius: 8px;\n'
        self.css += '    overflow: hidden;\n'
        self.css += '    margin: 10px 0;\n'
        self.css += '    transition: box-shadow 0.3s ease;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-panel:hover {\n'
        self.css += '    box-shadow: 0 2px 8px rgba(0,0,0,0.1);\n'
        self.css += '}\n\n'
        
        self.css += '.nova-panel-header {\n'
        self.css += '    background: #f8f9fa;\n'
        self.css += '    padding: 10px 20px;\n'
        self.css += '    font-weight: bold;\n'
        self.css += '    border-bottom: 1px solid #ddd;\n'
        self.css += '}\n\n'
        
        self.css += '.nova-panel-body {\n'
        self.css += '    padding: 20px;\n'
        self.css += '}\n\n'
        
        # Group
        self.css += '.nova-group {\n'
        self.css += '    margin: 10px 0;\n'
        self.css += '    padding: 10px;\n'
        self.css += '    border: 1px solid #eee;\n'
        self.css += '    border-radius: 4px;\n'
        self.css += '}\n\n'
        
        # Position absolute for exact positioning
        self.css += '.nova-absolute {\n'
        self.css += '    position: absolute;\n'
        self.css += '}\n\n'
        
        # Process AST for specific styling
        for node in ast:
            self.process_node(node)
        
        return self.css
    
    def process_node(self, node):
        if node.node_type == 'Background':
            # Background is handled inline in HTML
            pass
        elif node.node_type == 'Page':
            for child in node.children:
                self.process_node(child)
        elif hasattr(node, 'children'):
            for child in node.children:
                self.process_node(child)