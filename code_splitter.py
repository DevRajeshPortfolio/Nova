# code_splitter.py
# Nova Programming Language - Code Splitting

import os
import json
import hashlib
from pathlib import Path

class CodeSplitter:
    """Code splitting for Nova applications"""
    
    def __init__(self):
        self.chunks = {}
        self.routes = {}
        self.entry_points = {}
        self.dependencies = {}
        self.manifest = {}
    
    def split_by_routes(self, ast, routes=None):
        """Split code by routes"""
        if routes is None:
            routes = self._extract_routes(ast)
        
        for route_name, route_nodes in routes.items():
            chunk_name = self._generate_chunk_name(route_name)
            
            self.chunks[chunk_name] = {
                'name': chunk_name,
                'route': route_name,
                'nodes': route_nodes,
                'dependencies': self._extract_dependencies(route_nodes),
                'size': self._estimate_size(route_nodes)
            }
            
            self.routes[f'/{route_name}'] = {
                'chunk': chunk_name,
                'prefetch': self._get_prefetch_pages(route_nodes)
            }
        
        # Create entry point
        self._create_entry_point()
        
        # Generate manifest
        self.manifest = {
            'chunks': self.chunks,
            'routes': self.routes,
            'entry': 'main'
        }
        
        return self.manifest
    
    def _extract_routes(self, ast):
        """Extract routes from AST"""
        routes = {}
        
        for node in ast:
            if node.node_type == 'Page':
                page_name = node.name
                routes[page_name] = node.children
            elif hasattr(node, 'children'):
                # Recursively extract
                child_routes = self._extract_routes(node.children)
                routes.update(child_routes)
        
        return routes
    
    def _generate_chunk_name(self, route_name):
        """Generate a chunk name"""
        return f"chunk_{route_name}_{hashlib.md5(route_name.encode()).hexdigest()[:8]}"
    
    def _extract_dependencies(self, nodes):
        """Extract dependencies from nodes"""
        dependencies = set()
        
        for node in nodes:
            if hasattr(node, 'children'):
                deps = self._extract_dependencies(node.children)
                dependencies.update(deps)
            
            # Check for component usage
            if node.node_type == 'Use':
                dependencies.add(node.name)
            elif node.node_type == 'Component':
                dependencies.add(node.name)
        
        return list(dependencies)
    
    def _estimate_size(self, nodes):
        """Estimate size of nodes"""
        total = 0
        for node in nodes:
            # Rough estimate
            total += len(str(vars(node))) 
            if hasattr(node, 'children'):
                total += self._estimate_size(node.children)
        return total
    
    def _get_prefetch_pages(self, nodes):
        """Get pages to prefetch"""
        prefetch = []
        
        for node in nodes:
            if node.node_type == 'Link':
                url = getattr(node, 'url', '')
                if url and url.startswith('/'):
                    prefetch.append(url[1:])
            elif hasattr(node, 'children'):
                prefetch.extend(self._get_prefetch_pages(node.children))
        
        return list(set(prefetch))
    
    def _create_entry_point(self):
        """Create entry point"""
        self.entry_points['main'] = {
            'chunks': list(self.chunks.keys()),
            'preload': ['main']
        }
    
    def generate_loader(self):
        """Generate JavaScript loader for chunks"""
        return f'''
        // Nova Code Loader
        const manifest = {json.dumps(self.manifest, indent=2)};
        
        const loadedChunks = new Set();
        const pendingChunks = new Map();
        
        function loadChunk(chunkName) {{
            if (loadedChunks.has(chunkName)) {{
                return Promise.resolve();
            }}
            
            if (pendingChunks.has(chunkName)) {{
                return pendingChunks.get(chunkName);
            }}
            
            const promise = new Promise((resolve, reject) => {{
                const script = document.createElement('script');
                script.src = `/chunks/${{chunkName}}.js`;
                script.onload = () => {{
                    loadedChunks.add(chunkName);
                    pendingChunks.delete(chunkName);
                    resolve();
                }};
                script.onerror = () => {{
                    pendingChunks.delete(chunkName);
                    reject(new Error(`Failed to load chunk: ${{chunkName}}`));
                }};
                document.head.appendChild(script);
            }});
            
            pendingChunks.set(chunkName, promise);
            return promise;
        }}
        
        function loadRoute(route) {{
            const routeInfo = manifest.routes[route];
            if (!routeInfo) {{
                return Promise.reject(new Error(`Route not found: ${{route}}`));
            }}
            
            return loadChunk(routeInfo.chunk);
        }}
        
        function prefetchRoute(route) {{
            const routeInfo = manifest.routes[route];
            if (routeInfo) {{
                // Load in background
                loadChunk(routeInfo.chunk).catch(() => {{}});
            }}
        }}
        
        function preloadRoutes() {{
            const preload = manifest.chunks['main']?.preload || [];
            for (const route of preload) {{
                prefetchRoute(route);
            }}
        }}
        
        // Export loader
        window.NovaLoader = {{
            loadChunk,
            loadRoute,
            prefetchRoute,
            preloadRoutes,
            manifest
        }};
        
        // Auto-preload
        document.addEventListener('DOMContentLoaded', preloadRoutes);
        '''
    
    def generate_chunk_files(self, chunks, output_dir):
        """Generate chunk files"""
        os.makedirs(os.path.join(output_dir, 'chunks'), exist_ok=True)
        
        for chunk_name, chunk_data in chunks.items():
            chunk_path = os.path.join(output_dir, 'chunks', f'{chunk_name}.js')
            
            # Generate chunk content
            content = f'''
            // Chunk: {chunk_name}
            // Route: {chunk_data['route']}
            
            // Load dependencies
            const dependencies = {json.dumps(chunk_data['dependencies'])};
            for (const dep of dependencies) {{
                if (window.NovaLoader) {{
                    window.NovaLoader.loadChunk(dep).catch(() => {{}});
                }}
            }}
            
            // Render component
            if (window.NovaRuntime) {{
                window.NovaRuntime.renderRoute('{chunk_data['route']}');
            }}
            
            console.log('✅ Loaded chunk: {chunk_name}');
            '''
            
            with open(chunk_path, 'w') as f:
                f.write(content)
    
    def generate_manifest_file(self, output_dir):
        """Generate manifest file"""
        manifest_path = os.path.join(output_dir, 'manifest.json')
        with open(manifest_path, 'w') as f:
            json.dump(self.manifest, f, indent=2)