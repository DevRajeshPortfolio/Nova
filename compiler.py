# compiler.py
# Nova Programming Language - Main Compiler

import os
from lexer import Lexer
from parser import Parser
from html_generator import HTMLGenerator
from css_generator import CSSGenerator
from js_generator import JSGenerator


class Compiler:
    def __init__(self):
        self.html_generator = HTMLGenerator()
        self.css_generator = CSSGenerator()
        self.js_generator = JSGenerator()
    
    def compile(self, source_path, output_dir='output'):
        """Compile a Nova source file"""
        # Read source
        with open(source_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Lex
        lexer = Lexer(source_path, source)
        tokens, error = lexer.make_tokens()
        
        if error:
            print(error.as_string())
            return False
        
        # Parse
        parser = Parser(tokens)
        ast = parser.parse()
        
        if parser.errors:
            for err in parser.errors:
                print(f"Parse Error: {err}")
            return False
        
        # Generate output
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate HTML
        html = self.html_generator.generate(ast)
        with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        
        # Generate CSS
        css = self.css_generator.generate(ast)
        with open(os.path.join(output_dir, 'style.css'), 'w', encoding='utf-8') as f:
            f.write(css)
        
        # Generate JavaScript
        js = self.js_generator.generate(ast)
        with open(os.path.join(output_dir, 'script.js'), 'w', encoding='utf-8') as f:
            f.write(js)
        
        print(f"✅ Compiled successfully!")
        print(f"📁 Output directory: {output_dir}")
        print(f"📄 Generated files: index.html, style.css, script.js")
        
        return True


def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python compiler.py <source.nova> [output_dir]")
        return
    
    source_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else 'output'
    
    compiler = Compiler()
    compiler.compile(source_file, output_dir)


if __name__ == '__main__':
    main()



    def compile_runtime(self, source_path, output_dir='dist'):
        """Compile to runtime bundle (browser-executable)"""
        from nova_runtime import NovaRuntime
        
        runtime = NovaRuntime()
        output_path = os.path.join(output_dir, 'index.html')
        return runtime.compile_for_browser(source_path, output_path)