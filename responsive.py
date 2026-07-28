# responsive.py
# Nova Programming Language - Responsive Design

class Breakpoints:
    """Responsive breakpoints"""
    
    DEFAULT = {
        'mobile': 320,
        'phablet': 480,
        'tablet': 768,
        'desktop': 1024,
        'wide': 1200,
        'full': 1400
    }
    
    def __init__(self, breakpoints=None):
        self.breakpoints = breakpoints or self.DEFAULT.copy()
    
    def get_breakpoint(self, name):
        """Get breakpoint value"""
        return self.breakpoints.get(name, 0)
    
    def add_breakpoint(self, name, value):
        """Add a custom breakpoint"""
        self.breakpoints[name] = value
    
    def get_media_query(self, breakpoint, min_width=True):
        """Generate media query string"""
        value = self.get_breakpoint(breakpoint)
        if min_width:
            return f"@media (min-width: {value}px)"
        return f"@media (max-width: {value - 1}px)"


class ResponsiveStyles:
    """Responsive styles generator"""
    
    def __init__(self, breakpoints=None):
        self.breakpoints = Breakpoints(breakpoints)
        self.styles = {}
    
    def add_style(self, selector, styles, breakpoint=None):
        """Add styles with optional breakpoint"""
        key = f"{selector}:{breakpoint}" if breakpoint else selector
        self.styles[key] = {
            'selector': selector,
            'styles': styles,
            'breakpoint': breakpoint
        }
    
    def generate_css(self):
        """Generate responsive CSS"""
        css = ""
        
        # Group styles by selector
        grouped = {}
        for key, style in self.styles.items():
            if style['selector'] not in grouped:
                grouped[style['selector']] = {}
            grouped[style['selector']][style['breakpoint']] = style['styles']
        
        # Generate CSS
        for selector, breakpoints in grouped.items():
            # Base styles
            base_styles = breakpoints.get(None, {})
            if base_styles:
                css += f"{selector} {{\n"
                for prop, value in base_styles.items():
                    css += f"    {prop}: {value};\n"
                css += "}\n\n"
            
            # Breakpoint styles
            for breakpoint, styles in breakpoints.items():
                if breakpoint:
                    media_query = self.breakpoints.get_media_query(breakpoint)
                    css += f"{media_query} {{\n"
                    css += f"    {selector} {{\n"
                    for prop, value in styles.items():
                        css += f"        {prop}: {value};\n"
                    css += "    }\n"
                    css += "}\n\n"
        
        return css


class ResponsiveComponent:
    """Base responsive component"""
    
    def __init__(self, breakpoints=None):
        self.breakpoints = breakpoints or Breakpoints()
        self.responsive_styles = ResponsiveStyles(breakpoints)
    
    def get_responsive_value(self, values, breakpoint):
        """Get value for breakpoint"""
        # values: {'base': value, 'tablet': value, 'desktop': value}
        if breakpoint in values:
            return values[breakpoint]
        return values.get('base', None)
    
    def apply_responsive_styles(self, element, styles, current_breakpoint):
        """Apply responsive styles to element"""
        for prop, values in styles.items():
            value = self.get_responsive_value(values, current_breakpoint)
            if value:
                element.style[prop] = value


def generate_responsive_grid(columns, breakpoints=None):
    """Generate responsive grid CSS"""
    if breakpoints is None:
        breakpoints = {'mobile': 1, 'tablet': 2, 'desktop': 4}
    
    css = ".responsive-grid {\n"
    css += "    display: grid;\n"
    css += f"    grid-template-columns: repeat({breakpoints.get('mobile', 1)}, 1fr);\n"
    css += "    gap: 20px;\n"
    css += "}\n\n"
    
    for breakpoint, cols in breakpoints.items():
        if breakpoint != 'mobile':
            css += f"@media (min-width: {Breakpoints.DEFAULT.get(breakpoint, 768)}px) {{\n"
            css += "    .responsive-grid {\n"
            css += f"        grid-template-columns: repeat({cols}, 1fr);\n"
            css += "    }\n"
            css += "}\n\n"
    
    return css


def generate_responsive_container(breakpoints=None):
    """Generate responsive container CSS"""
    if breakpoints is None:
        breakpoints = {
            'mobile': '100%',
            'tablet': '720px',
            'desktop': '960px',
            'wide': '1140px'
        }
    
    css = ".responsive-container {\n"
    css += "    margin: 0 auto;\n"
    css += f"    max-width: {breakpoints.get('mobile', '100%')};\n"
    css += "    padding: 0 20px;\n"
    css += "}\n\n"
    
    for breakpoint, width in breakpoints.items():
        if breakpoint != 'mobile':
            value = Breakpoints.DEFAULT.get(breakpoint, 768)
            css += f"@media (min-width: {value}px) {{\n"
            css += "    .responsive-container {\n"
            css += f"        max-width: {width};\n"
            css += "    }\n"
            css += "}\n\n"
    
    return css


class ResponsiveImage:
    """Responsive image generator"""
    
    def __init__(self, src, alt='', sizes=None):
        self.src = src
        self.alt = alt
        self.sizes = sizes or {
            'mobile': '100vw',
            'tablet': '50vw',
            'desktop': '33vw'
        }
        self.srcset = {}
    
    def add_srcset(self, src, width):
        """Add srcset entry"""
        self.srcset[width] = src
    
    def generate_html(self):
        """Generate responsive image HTML"""
        srcset = ", ".join([f"{src} {w}w" for w, src in self.srcset.items()])
        sizes = ", ".join([f"(min-width: {Breakpoints.DEFAULT.get(bp, 0)}px) {size}" 
                          for bp, size in self.sizes.items()])
        
        return f"""
        <img src="{self.src}" 
             srcset="{srcset}" 
             sizes="{sizes}" 
             alt="{self.alt}"
             loading="lazy"
             class="responsive-image">
        """