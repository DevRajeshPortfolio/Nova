# optimizer.py
# Nova Programming Language - Asset Optimization

import os
import re
import json
import hashlib
from pathlib import Path

class AssetOptimizer:
    """Asset optimizer for Nova applications"""
    
    def __init__(self):
        self.minify_js = True
        self.minify_css = True
        self.optimize_images = True
        self.optimize_fonts = True
        self.compress_assets = True
    
    def optimize_assets(self, assets_dir, output_dir):
        """Optimize all assets"""
        optimized = {}
        
        for root, dirs, files in os.walk(assets_dir):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, assets_dir)
                
                if file.endswith(('.css', '.scss')):
                    optimized[rel_path] = self.optimize_css(file_path)
                elif file.endswith(('.js', '.mjs')):
                    optimized[rel_path] = self.optimize_js(file_path)
                elif file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')):
                    optimized[rel_path] = self.optimize_image(file_path)
                elif file.endswith(('.woff', '.woff2', '.ttf', '.otf')):
                    optimized[rel_path] = self.optimize_font(file_path)
                elif file.endswith('.html'):
                    optimized[rel_path] = self.optimize_html(file_path)
                else:
                    # Copy as-is
                    with open(file_path, 'rb') as f:
                        optimized[rel_path] = f.read()
        
        # Write optimized assets
        for rel_path, content in optimized.items():
            out_path = os.path.join(output_dir, rel_path)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            
            if isinstance(content, str):
                with open(out_path, 'w') as f:
                    f.write(content)
            else:
                with open(out_path, 'wb') as f:
                    f.write(content)
        
        return optimized
    
    def optimize_css(self, file_path):
        """Optimize CSS file"""
        with open(file_path, 'r') as f:
            content = f.read()
        
        if self.minify_css:
            content = self._minify_css(content)
        
        return content
    
    def _minify_css(self, css):
        """Minify CSS"""
        # Remove comments
        css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
        
        # Remove whitespace
        css = re.sub(r'\s+', ' ', css)
        
        # Remove spaces around selectors
        css = re.sub(r'\s*{\s*', '{', css)
        css = re.sub(r'\s*}\s*', '}', css)
        css = re.sub(r'\s*;\s*', ';', css)
        css = re.sub(r'\s*:\s*', ':', css)
        css = re.sub(r'\s*,\s*', ',', css)
        
        # Remove trailing semicolons
        css = re.sub(r';\s*}', '}', css)
        
        return css.strip()
    
    def optimize_js(self, file_path):
        """Optimize JavaScript file"""
        with open(file_path, 'r') as f:
            content = f.read()
        
        if self.minify_js:
            content = self._minify_js(content)
        
        return content
    
    def _minify_js(self, js):
        """Minify JavaScript"""
        # Remove comments
        js = re.sub(r'//.*?\n', '\n', js)
        js = re.sub(r'/\*.*?\*/', '', js, flags=re.DOTALL)
        
        # Remove whitespace
        js = re.sub(r'\s+', ' ', js)
        
        # Remove spaces around operators
        js = re.sub(r'\s*=\s*', '=', js)
        js = re.sub(r'\s*\+\s*', '+', js)
        js = re.sub(r'\s*-\s*', '-', js)
        js = re.sub(r'\s*\*\s*', '*', js)
        js = re.sub(r'\s*/\s*', '/', js)
        
        return js.strip()
    
    def optimize_image(self, file_path):
        """Optimize image"""
        # For simplicity, just read the file
        # In production, use PIL/Pillow for image optimization
        with open(file_path, 'rb') as f:
            return f.read()
    
    def optimize_font(self, file_path):
        """Optimize font"""
        # For simplicity, just read the file
        with open(file_path, 'rb') as f:
            return f.read()
    
    def optimize_html(self, file_path):
        """Optimize HTML"""
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Minify HTML
        if self.minify_html:
            content = self._minify_html(content)
        
        return content
    
    def _minify_html(self, html):
        """Minify HTML"""
        # Remove comments
        html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
        
        # Remove whitespace between tags
        html = re.sub(r'>\s+<', '><', html)
        
        # Remove unnecessary quotes
        html = re.sub(r'"([^"]*?)"', lambda m: f'"{m.group(1)}"', html)
        
        return html.strip()


class ImageOptimizer:
    """Image optimization utilities"""
    
    def __init__(self, quality=80, formats=None):
        self.quality = quality
        self.formats = formats or ['webp', 'avif']
    
    def optimize(self, image_data, format='webp'):
        """Optimize an image"""
        # Placeholder - would use PIL/Pillow in production
        return image_data
    
    def create_responsive(self, image_data, sizes):
        """Create responsive image variants"""
        variants = {}
        for size in sizes:
            variants[f'{size}w'] = self.resize(image_data, size)
        return variants
    
    def resize(self, image_data, width):
        """Resize an image"""
        # Placeholder
        return image_data
    
    def to_webp(self, image_data):
        """Convert to WebP format"""
        return self.optimize(image_data, 'webp')
    
    def to_avif(self, image_data):
        """Convert to AVIF format"""
        return self.optimize(image_data, 'avif')


class CSSOptimizer:
    """CSS optimization utilities"""
    
    def __init__(self):
        self.compress_colors = True
        self.remove_unused = True
        self.combine_selectors = True
    
    def minify(self, css):
        """Minify CSS"""
        # Remove comments
        css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
        
        # Remove whitespace
        css = re.sub(r'\s+', ' ', css)
        
        # Remove spaces around selectors
        css = re.sub(r'\s*{\s*', '{', css)
        css = re.sub(r'\s*}\s*', '}', css)
        css = re.sub(r'\s*;\s*', ';', css)
        css = re.sub(r'\s*:\s*', ':', css)
        css = re.sub(r'\s*,\s*', ',', css)
        
        # Remove trailing semicolons
        css = re.sub(r';\s*}', '}', css)
        
        return css.strip()
    
    def compress_colors(self, css):
        """Compress color values"""
        # Hex to short hex
        css = re.sub(r'#([0-9a-fA-F])\1([0-9a-fA-F])\2([0-9a-fA-F])\3', r'#\1\2\3', css)
        return css


class JSOptimizer:
    """JavaScript optimization utilities"""
    
    def __init__(self):
        self.tree_shaking = True
        self.dead_code_elimination = True
        self.rename_variables = True
    
    def minify(self, js):
        """Minify JavaScript"""
        # Remove comments
        js = re.sub(r'//.*?\n', '\n', js)
        js = re.sub(r'/\*.*?\*/', '', js, flags=re.DOTALL)
        
        # Remove whitespace
        js = re.sub(r'\s+', ' ', js)
        
        # Remove spaces around operators
        js = re.sub(r'\s*=\s*', '=', js)
        js = re.sub(r'\s*\+\s*', '+', js)
        js = re.sub(r'\s*-\s*', '-', js)
        js = re.sub(r'\s*\*\s*', '*', js)
        js = re.sub(r'\s*/\s*', '/', js)
        
        return js.strip()
    
    def optimize_imports(self, js):
        """Optimize imports"""
        # Remove unused imports
        # This would need full AST analysis
        return js


class AssetPipeline:
    """Complete asset pipeline"""
    
    def __init__(self):
        self.optimizer = AssetOptimizer()
        self.image_optimizer = ImageOptimizer()
        self.css_optimizer = CSSOptimizer()
        self.js_optimizer = JSOptimizer()
    
    def process(self, source_dir, output_dir):
        """Process all assets"""
        print("📦 Processing assets...")
        
        # Optimize everything
        self.optimizer.optimize_assets(source_dir, output_dir)
        
        print(f"✅ Assets processed to {output_dir}")