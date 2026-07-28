# theme.py
# Nova Programming Language - CSS Theming System

import re
import json

class Theme:
    """CSS Theme definition"""
    
    def __init__(self, name, config=None):
        self.name = name
        self.config = config or {}
        self.variables = {}
        self._parse_config()
    
    def _parse_config(self):
        """Parse theme configuration"""
        # Common theme variables
        self.variables = {
            'primary': self.config.get('primary', '#007bff'),
            'secondary': self.config.get('secondary', '#6c757d'),
            'success': self.config.get('success', '#28a745'),
            'danger': self.config.get('danger', '#dc3545'),
            'warning': self.config.get('warning', '#ffc107'),
            'info': self.config.get('info', '#17a2b8'),
            'light': self.config.get('light', '#f8f9fa'),
            'dark': self.config.get('dark', '#343a40'),
            'background': self.config.get('background', '#ffffff'),
            'text': self.config.get('text', '#333333'),
            'font_family': self.config.get('font', 'system-ui, -apple-system, sans-serif'),
            'border_radius': self.config.get('borderRadius', '4px'),
            'box_shadow': self.config.get('boxShadow', '0 2px 4px rgba(0,0,0,0.1)'),
            'transition': self.config.get('transition', '0.3s ease'),
            'container_width': self.config.get('containerWidth', '1200px'),
            'spacing': self.config.get('spacing', '20px'),
            'heading_font': self.config.get('headingFont', 'inherit'),
        }
    
    def to_css(self):
        """Convert theme to CSS variables"""
        css = f"""
        :root {{
            --theme-name: {self.name};
            --primary: {self.variables['primary']};
            --secondary: {self.variables['secondary']};
            --success: {self.variables['success']};
            --danger: {self.variables['danger']};
            --warning: {self.variables['warning']};
            --info: {self.variables['info']};
            --light: {self.variables['light']};
            --dark: {self.variables['dark']};
            --background: {self.variables['background']};
            --text: {self.variables['text']};
            --font-family: {self.variables['font_family']};
            --border-radius: {self.variables['border_radius']};
            --box-shadow: {self.variables['box_shadow']};
            --transition: {self.variables['transition']};
            --container-width: {self.variables['container_width']};
            --spacing: {self.variables['spacing']};
            --heading-font: {self.variables['heading_font']};
        }}
        """
        return css
    
    def generate_theme_styles(self):
        """Generate theme-specific styles"""
        css = self.to_css()
        
        # Add theme classes
        css += f"""
        .theme-{self.name} {{
            background-color: var(--background);
            color: var(--text);
            font-family: var(--font-family);
        }}
        
        .theme-{self.name} .nova-button {{
            background-color: var(--primary);
            color: white;
            border-radius: var(--border-radius);
            transition: var(--transition);
        }}
        
        .theme-{self.name} .nova-button:hover {{
            background-color: {self._darken_color(self.variables['primary'])};
        }}
        
        .theme-{self.name} .nova-input {{
            border: 1px solid var(--secondary);
            border-radius: var(--border-radius);
            transition: var(--transition);
        }}
        
        .theme-{self.name} .nova-input:focus {{
            border-color: var(--primary);
            box-shadow: 0 0 0 2px {self._rgba_color(self.variables['primary'], 0.25)};
        }}
        
        .theme-{self.name} .nova-card {{
            background: white;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            transition: var(--transition);
        }}
        
        .theme-{self.name} .nova-card:hover {{
            box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        }}
        """
        return css
    
    def _darken_color(self, color, amount=0.2):
        """Darken a color by amount"""
        # Simple implementation - could use color library
        return color  # Placeholder
    
    def _rgba_color(self, color, alpha):
        """Convert color to RGBA"""
        # Simple implementation
        return color  # Placeholder


class ThemeManager:
    """Theme manager"""
    
    def __init__(self):
        self.themes = {}
        self.active_theme = None
        self.default_theme = 'light'
    
    def register_theme(self, name, config):
        """Register a theme"""
        theme = Theme(name, config)
        self.themes[name] = theme
        return theme
    
    def get_theme(self, name):
        """Get a theme by name"""
        return self.themes.get(name)
    
    def set_active_theme(self, name):
        """Set the active theme"""
        if name in self.themes:
            self.active_theme = name
            return True
        return False
    
    def get_active_theme(self):
        """Get the active theme"""
        if self.active_theme:
            return self.themes.get(self.active_theme)
        return self.themes.get(self.default_theme)
    
    def generate_all_css(self):
        """Generate CSS for all themes"""
        css = ""
        for name, theme in self.themes.items():
            css += f"/* Theme: {name} */\n"
            css += theme.generate_theme_styles()
            css += "\n"
        return css
    
    def generate_theme_switch_js(self):
        """Generate JavaScript for theme switching"""
        return """
        function switchTheme(themeName) {
            // Remove existing theme classes
            document.body.className = document.body.className
                .split(' ')
                .filter(cls => !cls.startsWith('theme-'))
                .join(' ');
            
            // Add new theme class
            document.body.classList.add('theme-' + themeName);
            
            // Save preference
            localStorage.setItem('nova_theme', themeName);
        }
        
        function loadThemePreference() {
            const savedTheme = localStorage.getItem('nova_theme');
            if (savedTheme) {
                switchTheme(savedTheme);
            }
        }
        
        // Load theme on page load
        document.addEventListener('DOMContentLoaded', loadThemePreference);
        """


class CSSGeneratorWithTheme:
    """CSS generator with theme support"""
    
    def __init__(self):
        self.theme_manager = ThemeManager()
        self.component_styles = {}
        self.mixins = {}
    
    def add_theme(self, name, config):
        """Add a theme"""
        return self.theme_manager.register_theme(name, config)
    
    def set_active_theme(self, name):
        """Set active theme"""
        return self.theme_manager.set_active_theme(name)
    
    def add_component_styles(self, component_name, styles):
        """Add component-specific styles"""
        self.component_styles[component_name] = styles
    
    def add_mixin(self, name, styles):
        """Add a CSS mixin"""
        self.mixins[name] = styles
    
    def generate_css(self):
        """Generate complete CSS"""
        css = "/* Nova Generated CSS with Themes */\n\n"
        
        # Generate theme CSS
        css += self.theme_manager.generate_all_css()
        
        # Generate component styles
        css += "\n/* Component Styles */\n"
        for name, styles in self.component_styles.items():
            css += f"\n/* {name} */\n"
            css += styles
        
        # Generate mixins
        css += "\n/* Mixins */\n"
        for name, styles in self.mixins.items():
            css += f"\n/* Mixin: {name} */\n"
            css += styles
        
        return css
    
    def generate_theme_switch_html(self):
        """Generate HTML for theme switcher"""
        themes_html = ""
        for name in self.theme_manager.themes.keys():
            themes_html += f"""
            <button class="theme-btn" data-theme="{name}" onclick="switchTheme('{name}')">
                {name.capitalize()}
            </button>
            """
        
        return f"""
        <div class="theme-switcher">
            {themes_html}
        </div>
        <style>
            .theme-switcher {{
                position: fixed;
                top: 10px;
                right: 10px;
                display: flex;
                gap: 5px;
                z-index: 1000;
            }}
            .theme-btn {{
                padding: 5px 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background: white;
                cursor: pointer;
                font-size: 12px;
            }}
            .theme-btn:hover {{
                background: #f0f0f0;
            }}
        </style>
        """