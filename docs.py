# docs.py
# Nova Programming Language - Documentation Generator

import os
import json
import re
from datetime import datetime

class DocGenerator:
    """Documentation generator for Nova"""
    
    def __init__(self):
        self.docs = {}
        self.examples = []
        self.api_reference = {}
        self.tutorials = []
    
    def generate_from_ast(self, ast):
        """Generate documentation from AST"""
        for node in ast:
            self._process_node(node)
        
        return self.docs
    
    def _process_node(self, node):
        """Process a node for documentation"""
        doc = {
            'type': node.node_type,
            'name': getattr(node, 'name', None),
            'description': self._extract_docstring(node),
            'parameters': self._extract_parameters(node),
            'returns': self._extract_return_type(node),
            'example': self._extract_example(node),
            'see_also': self._extract_see_also(node)
        }
        
        # Store by type
        if doc['type'] not in self.docs:
            self.docs[doc['type']] = []
        
        # Avoid duplicates
        if doc not in self.docs[doc['type']]:
            self.docs[doc['type']].append(doc)
        
        # Process children
        if hasattr(node, 'children'):
            for child in node.children:
                self._process_node(child)
    
    def _extract_docstring(self, node):
        """Extract docstring from node"""
        # Look for comment node before this node
        # For simplicity, check if node has a 'comment' attribute
        if hasattr(node, 'comment'):
            return node.comment
        return ''
    
    def _extract_parameters(self, node):
        """Extract parameters from node"""
        params = []
        if hasattr(node, 'params'):
            for param in node.params:
                params.append({
                    'name': param,
                    'type': getattr(param, 'type', 'any'),
                    'description': ''
                })
        elif hasattr(node, 'properties'):
            for key, value in node.properties.items():
                if isinstance(value, dict) and 'type' in value:
                    params.append({
                        'name': key,
                        'type': value['type'],
                        'description': value.get('description', '')
                    })
        return params
    
    def _extract_return_type(self, node):
        """Extract return type from node"""
        if hasattr(node, 'return_type'):
            return node.return_type
        return None
    
    def _extract_example(self, node):
        """Extract example from node"""
        if hasattr(node, 'example'):
            return node.example
        return None
    
    def _extract_see_also(self, node):
        """Extract see also references"""
        if hasattr(node, 'see_also'):
            return node.see_also
        return []
    
    def generate_markdown(self):
        """Generate Markdown documentation"""
        md = ["# Nova Language Documentation\n"]
        md.append(f"Generated: {datetime.now().isoformat()}\n")
        
        # Table of contents
        md.append("## Table of Contents\n")
        for doc_type in sorted(self.docs.keys()):
            md.append(f"- [{doc_type}](#{doc_type.lower()})")
        md.append("")
        
        # Documentation by type
        for doc_type, docs in sorted(self.docs.items()):
            md.append(f"## {doc_type}\n")
            for doc in docs:
                if doc.get('name'):
                    md.append(f"### {doc['name']}\n")
                
                if doc.get('description'):
                    md.append(f"{doc['description']}\n")
                
                if doc.get('parameters'):
                    md.append("**Parameters:**\n")
                    for param in doc['parameters']:
                        param_type = f" ({param['type']})" if param.get('type') else ""
                        md.append(f"- `{param['name']}`{param_type}: {param.get('description', '')}")
                    md.append("")
                
                if doc.get('returns'):
                    md.append(f"**Returns:** `{doc['returns']}`\n")
                
                if doc.get('example'):
                    md.append("**Example:**\n")
                    md.append("```nova")
                    md.append(doc['example'])
                    md.append("```\n")
                
                if doc.get('see_also'):
                    md.append("**See Also:** " + ", ".join(doc['see_also']) + "\n")
                
                md.append("---\n")
        
        return '\n'.join(md)
    
    def generate_html(self):
        """Generate HTML documentation"""
        html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nova Language Documentation</title>
    <style>
        body {{
            font-family: system-ui, -apple-system, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }}
        .doc-section {{
            margin: 20px 0;
            padding: 20px;
            border: 1px solid #eee;
            border-radius: 8px;
            background: #fafafa;
        }}
        .doc-item {{
            margin: 15px 0;
            padding: 15px;
            background: white;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .param {{
            margin: 5px 0;
            padding: 5px 10px;
            background: #f0f0f0;
            border-radius: 4px;
        }}
        .example {{
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
        }}
        .toc {{
            background: #f0f0f0;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .toc a {{
            text-decoration: none;
            color: #007bff;
        }}
        .toc a:hover {{
            text-decoration: underline;
        }}
        .type-badge {{
            background: #007bff;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <h1>📚 Nova Language Documentation</h1>
    <p>Generated: {datetime.now().isoformat()}</p>
    
    <div class="toc">
        <h2>Table of Contents</h2>
        <ul>
'''
        for doc_type in sorted(self.docs.keys()):
            html += f'            <li><a href="#{doc_type.lower()}">{doc_type}</a></li>\n'
        
        html += '''        </ul>
    </div>
    
'''
        for doc_type, docs in sorted(self.docs.items()):
            html += f'''    <div class="doc-section" id="{doc_type.lower()}">
        <h2>{doc_type}</h2>
'''
            for doc in docs:
                html += '        <div class="doc-item">\n'
                
                if doc.get('name'):
                    html += f'            <h3>{doc["name"]}</h3>\n'
                
                if doc.get('description'):
                    html += f'            <p>{doc["description"]}</p>\n'
                
                if doc.get('parameters'):
                    html += '            <h4>Parameters</h4>\n'
                    for param in doc['parameters']:
                        param_type = f' <span class="type-badge">{param["type"]}</span>' if param.get('type') else ''
                        html += f'            <div class="param">`{param["name"]}`{param_type}: {param.get("description", "")}</div>\n'
                
                if doc.get('returns'):
                    html += f'            <p><strong>Returns:</strong> <code>{doc["returns"]}</code></p>\n'
                
                if doc.get('example'):
                    html += '            <h4>Example</h4>\n'
                    html += f'            <div class="example"><pre>{doc["example"]}</pre></div>\n'
                
                if doc.get('see_also'):
                    html += '            <p><strong>See Also:</strong> ' + ', '.join(doc['see_also']) + '</p>\n'
                
                html += '        </div>\n'
            
            html += '    </div>\n'
        
        html += '''
    <footer>
        <p>Generated by Nova Documentation Generator</p>
    </footer>
</body>
</html>'''
        
        return html
    
    def generate_json(self):
        """Generate JSON documentation"""
        return json.dumps(self.docs, indent=2)
    
    def generate(self, output_format='html'):
        """Generate documentation in specified format"""
        if output_format == 'html':
            return self.generate_html()
        elif output_format == 'markdown':
            return self.generate_markdown()
        elif output_format == 'json':
            return self.generate_json()
        else:
            return self.generate_html()
    
    def save(self, output_path, format='html'):
        """Save documentation to file"""
        content = self.generate(format)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Documentation saved to {output_path}")
        return output_path


class InteractiveDocs:
    """Interactive documentation server"""
    
    def __init__(self, doc_generator):
        self.doc_generator = doc_generator
        self.port = 3001
    
    def start_server(self):
        """Start interactive documentation server"""
        # Create a simple HTTP server for docs
        import http.server
        import socketserver
        
        class Handler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/':
                    self.path = '/docs.html'
                return super().do_GET()
        
        # Generate HTML docs
        html = self.doc_generator.generate_html()
        with open('docs.html', 'w') as f:
            f.write(html)
        
        print(f"📚 Documentation server running at http://localhost:{self.port}")
        print("Press Ctrl+C to stop")
        
        try:
            with socketserver.TCPServer(("", self.port), Handler) as httpd:
                httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Documentation server stopped")