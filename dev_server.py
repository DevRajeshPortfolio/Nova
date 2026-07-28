# dev_server.py
# Nova Programming Language - Development Server with Hot Reload

import os
import sys
import time
import json
import threading
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DevServer:
    """Development server with hot reload"""
    
    def __init__(self, source_dir='.', output_dir='dist', port=3000):
        self.source_dir = os.path.abspath(source_dir)
        self.output_dir = os.path.abspath(output_dir)
        self.port = port
        self.compiler = None
        self._observer = None
        self._running = False
        self._watched_files = set()
        self._compile_queue = []
        self._is_compiling = False
        self._clients = []
    
    def start(self):
        """Start the development server"""
        print(f"🚀 Starting Nova Dev Server on http://localhost:{self.port}")
        print(f"📁 Source directory: {self.source_dir}")
        print(f"📁 Output directory: {self.output_dir}")
        print("📝 Watching for changes...")
        
        # Import compiler
        from compiler import Compiler
        self.compiler = Compiler()
        
        # Initial compile
        self._compile_all()
        
        # Start file watcher
        self._start_watcher()
        
        # Start HTTP server with WebSocket
        self._start_server()
    
    def _compile_all(self):
        """Compile all Nova files"""
        nova_files = self._find_nova_files()
        
        if not nova_files:
            print("⚠️ No Nova files found")
            return
        
        for file_path in nova_files:
            self._compile_file(file_path)
        
        print(f"✅ Compiled {len(nova_files)} files")
    
    def _find_nova_files(self):
        """Find all Nova files in source directory"""
        nova_files = []
        for root, dirs, files in os.walk(self.source_dir):
            for file in files:
                if file.endswith('.nova'):
                    nova_files.append(os.path.join(root, file))
        return nova_files
    
    def _compile_file(self, file_path):
        """Compile a single file"""
        try:
            rel_path = os.path.relpath(file_path, self.source_dir)
            output_path = os.path.join(self.output_dir, rel_path.replace('.nova', '.html'))
            
            # Compile
            self.compiler.compile(file_path, os.path.dirname(output_path))
            
            return True
        except Exception as e:
            print(f"❌ Compilation error in {file_path}: {e}")
            return False
    
    def _start_watcher(self):
        """Start the file watcher"""
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
        
        class NovaFileHandler(FileSystemEventHandler):
            def __init__(self, dev_server):
                self.dev_server = dev_server
            
            def on_modified(self, event):
                if event.src_path.endswith('.nova'):
                    print(f"🔄 File changed: {event.src_path}")
                    self.dev_server._handle_file_change(event.src_path)
            
            def on_created(self, event):
                if event.src_path.endswith('.nova'):
                    print(f"📄 New file: {event.src_path}")
                    self.dev_server._handle_file_change(event.src_path)
        
        self._observer = Observer()
        self._observer.schedule(
            NovaFileHandler(self),
            self.source_dir,
            recursive=True
        )
        self._observer.start()
    
    def _handle_file_change(self, file_path):
        """Handle a file change"""
        # Queue compilation
        if file_path not in self._compile_queue:
            self._compile_queue.append(file_path)
        
        # Process queue with debounce
        if not self._is_compiling:
            self._process_queue()
    
    def _process_queue(self):
        """Process the compile queue"""
        if not self._compile_queue:
            return
        
        self._is_compiling = True
        file_path = self._compile_queue.pop(0)
        
        # Compile
        success = self._compile_file(file_path)
        
        if success:
            # Notify clients
            self._notify_clients({
                'type': 'reload',
                'file': file_path,
                'timestamp': time.time()
            })
        
        self._is_compiling = False
        
        # Process next in queue
        if self._compile_queue:
            # Debounce: wait a bit before processing next
            time.sleep(0.1)
            self._process_queue()
    
    def _start_server(self):
        """Start the HTTP server"""
        import http.server
        import socketserver
        
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                self.dev_server = kwargs.pop('dev_server', None)
                super().__init__(*args, **kwargs)
            
            def do_GET(self):
                # Serve from output directory
                if self.path == '/':
                    self.path = '/index.html'
                
                # Check if file exists in output
                file_path = os.path.join(self.dev_server.output_dir, self.path.lstrip('/'))
                if os.path.isfile(file_path):
                    self._serve_file(file_path)
                else:
                    self.send_error(404, "File not found")
            
            def _serve_file(self, file_path):
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header('Content-Type', self._get_mime_type(file_path))
                self.send_header('Content-Length', len(content))
                self.end_headers()
                self.wfile.write(content)
            
            def _get_mime_type(self, file_path):
                ext = os.path.splitext(file_path)[1].lower()
                mime_types = {
                    '.html': 'text/html',
                    '.css': 'text/css',
                    '.js': 'application/javascript',
                    '.json': 'application/json',
                    '.png': 'image/png',
                    '.jpg': 'image/jpeg',
                    '.jpeg': 'image/jpeg',
                    '.gif': 'image/gif',
                    '.svg': 'image/svg+xml'
                }
                return mime_types.get(ext, 'application/octet-stream')
        
        try:
            with socketserver.TCPServer(("", self.port), 
                                       lambda *args, **kwargs: Handler(*args, dev_server=self, **kwargs)) as httpd:
                self._running = True
                print(f"🌐 Server running at http://localhost:{self.port}")
                print("Press Ctrl+C to stop")
                try:
                    httpd.serve_forever()
                except KeyboardInterrupt:
                    print("\n🛑 Stopping server...")
                    self._running = False
                    httpd.shutdown()
        except OSError as e:
            print(f"❌ Failed to start server: {e}")
    
    def _notify_clients(self, message):
        """Notify clients of changes (WebSocket)"""
        # Simple implementation: write to a file for polling
        # In production, use WebSocket
        reload_file = os.path.join(self.output_dir, '.reload')
        with open(reload_file, 'w') as f:
            json.dump(message, f)
    
    def stop(self):
        """Stop the development server"""
        self._running = False
        if self._observer:
            self._observer.stop()
            self._observer.join()
        print("✅ Dev server stopped")


def run_dev_server():
    """CLI command to run dev server"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Nova Dev Server')
    parser.add_argument('--source', '-s', default='.', help='Source directory')
    parser.add_argument('--output', '-o', default='dist', help='Output directory')
    parser.add_argument('--port', '-p', type=int, default=3000, help='Port number')
    
    args = parser.parse_args()
    
    server = DevServer(args.source, args.output, args.port)
    server.start()