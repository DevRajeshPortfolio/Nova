# server.py
# Nova Programming Language - HTTP Server

import json
import http.server
import socketserver
import urllib.parse
import os
from http import HTTPStatus
from functools import wraps
import threading
import time

class Route:
    """Route definition"""
    def __init__(self, path, method, handler, middleware=None):
        self.path = path
        self.method = method.upper()
        self.handler = handler
        self.middleware = middleware or []


class Request:
    """HTTP Request wrapper"""
    def __init__(self, headers, method, path, body=None, query_params=None):
        self.headers = headers
        self.method = method
        self.path = path
        self.body = body
        self.query_params = query_params or {}
        self.params = {}  # Route parameters
        self.user = None
        self.session = {}
        self.cookies = {}
    
    @property
    def json(self):
        """Parse body as JSON"""
        if self.body:
            try:
                return json.loads(self.body)
            except:
                return None
        return None
    
    def get_query(self, key, default=None):
        """Get query parameter"""
        return self.query_params.get(key, default)


class Response:
    """HTTP Response wrapper"""
    def __init__(self):
        self.status_code = 200
        self.headers = {'Content-Type': 'text/html'}
        self.body = ''
        self.cookies = []
    
    def set_status(self, code):
        self.status_code = code
        return self
    
    def set_header(self, key, value):
        self.headers[key] = value
        return self
    
    def set_cookie(self, name, value, **options):
        cookie = f"{name}={value}"
        if options.get('max_age'):
            cookie += f"; Max-Age={options['max_age']}"
        if options.get('path'):
            cookie += f"; Path={options['path']}"
        if options.get('secure'):
            cookie += "; Secure"
        if options.get('http_only'):
            cookie += "; HttpOnly"
        if options.get('same_site'):
            cookie += f"; SameSite={options['same_site']}"
        self.cookies.append(cookie)
        return self
    
    def json(self, data):
        self.headers['Content-Type'] = 'application/json'
        self.body = json.dumps(data)
        return self
    
    def html(self, content):
        self.headers['Content-Type'] = 'text/html'
        self.body = content
        return self
    
    def text(self, content):
        self.headers['Content-Type'] = 'text/plain'
        self.body = content
        return self
    
    def file(self, content, filename, mime_type='application/octet-stream'):
        self.headers['Content-Type'] = mime_type
        self.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        self.body = content
        return self
    
    def redirect(self, url):
        self.status_code = 302
        self.headers['Location'] = url
        return self
    
    def to_http(self):
        """Convert to HTTP response format"""
        status_line = f"HTTP/1.1 {self.status_code} {HTTPStatus(self.status_code).phrase}"
        
        headers = []
        for key, value in self.headers.items():
            headers.append(f"{key}: {value}")
        
        for cookie in self.cookies:
            headers.append(f"Set-Cookie: {cookie}")
        
        response = f"{status_line}\r\n"
        response += "\r\n".join(headers)
        response += "\r\n\r\n"
        response += self.body if isinstance(self.body, str) else str(self.body)
        
        return response.encode('utf-8')


class NovaHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler for Nova"""
    
    def __init__(self, *args, **kwargs):
        self.server_instance = kwargs.pop('server_instance', None)
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        self._handle_request('GET')
    
    def do_POST(self):
        self._handle_request('POST')
    
    def do_PUT(self):
        self._handle_request('PUT')
    
    def do_DELETE(self):
        self._handle_request('DELETE')
    
    def do_PATCH(self):
        self._handle_request('PATCH')
    
    def _handle_request(self, method):
        """Handle incoming request"""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query_params = urllib.parse.parse_qs(parsed.query)
        
        # Read body for POST/PUT/PATCH
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else None
        
        # Create request object
        request = Request(
            headers=self.headers,
            method=method,
            path=path,
            body=body,
            query_params={k: v[0] if v else None for k, v in query_params.items()}
        )
        
        # Parse cookies
        cookie_header = self.headers.get('Cookie', '')
        for cookie in cookie_header.split(';'):
            if '=' in cookie:
                key, value = cookie.strip().split('=', 1)
                request.cookies[key] = value
        
        # Find matching route
        response = self.server_instance.routes.handle_request(request)
        
        if response is None:
            # Try to serve static file
            if self._serve_static(path):
                return
            
            # 404 Not Found
            response = Response().set_status(404).text('404 Not Found')
        
        # Send response
        self.send_response(response.status_code)
        for key, value in response.headers.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(response.to_http())
    
    def _serve_static(self, path):
        """Serve static files"""
        static_dir = getattr(self.server_instance, 'static_dir', 'static')
        file_path = os.path.join(static_dir, path.lstrip('/'))
        
        # Security: prevent directory traversal
        if '..' in path:
            return False
        
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # Determine MIME type
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
                '.svg': 'image/svg+xml',
                '.ico': 'image/x-icon',
            }
            mime_type = mime_types.get(ext, 'application/octet-stream')
            
            self.send_response(200)
            self.send_header('Content-Type', mime_type)
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
            return True
        return False


class RouteManager:
    """Route manager"""
    
    def __init__(self):
        self.routes = {}
        self.middleware = []
    
    def add(self, path, method, handler, middleware=None):
        """Add a route"""
        key = f"{method.upper()}:{path}"
        self.routes[key] = Route(path, method, handler, middleware)
    
    def add_middleware(self, middleware):
        """Add global middleware"""
        self.middleware.append(middleware)
    
    def handle_request(self, request):
        """Handle a request"""
        # Apply middleware
        for middleware in self.middleware:
            response = middleware(request)
            if response is not None:
                return response
        
        # Find matching route
        for key, route in self.routes.items():
            if route.method == request.method.upper():
                # Simple path matching (support parameters: /users/:id)
                route_parts = route.path.split('/')
                request_parts = request.path.split('/')
                
                if len(route_parts) != len(request_parts):
                    continue
                
                params = {}
                match = True
                for rp, rq in zip(route_parts, request_parts):
                    if rp.startswith(':'):
                        params[rp[1:]] = rq
                    elif rp != rq:
                        match = False
                        break
                
                if match:
                    request.params = params
                    # Apply route middleware
                    for mw in route.middleware:
                        response = mw(request)
                        if response is not None:
                            return response
                    return route.handler(request)
        
        return None


class NovaServer:
    """Nova HTTP Server"""
    
    def __init__(self, host='localhost', port=3000):
        self.host = host
        self.port = port
        self.routes = RouteManager()
        self.static_dir = 'static'
        self._server = None
        self._running = False
    
    def route(self, path, method='GET'):
        """Decorator to register a route"""
        def decorator(handler):
            self.routes.add(path, method, handler)
            return handler
        return decorator
    
    def get(self, path):
        return self.route(path, 'GET')
    
    def post(self, path):
        return self.route(path, 'POST')
    
    def put(self, path):
        return self.route(path, 'PUT')
    
    def delete(self, path):
        return self.route(path, 'DELETE')
    
    def patch(self, path):
        return self.route(path, 'PATCH')
    
    def use(self, middleware):
        """Add global middleware"""
        self.routes.add_middleware(middleware)
    
    def serve_static(self, directory):
        """Set static files directory"""
        self.static_dir = directory
    
    def start(self, host=None, port=None):
        """Start the server"""
        if host is not None:
            self.host = host
        if port is not None:
            self.port = port
        
        class Handler(NovaHTTPRequestHandler):
            server_instance = self
        
        try:
            with socketserver.TCPServer((self.host, self.port), Handler) as httpd:
                self._server = httpd
                self._running = True
                print(f"🚀 Nova Server running at http://{self.host}:{self.port}")
                print(f"📁 Static files: {self.static_dir}")
                print("Press Ctrl+C to stop")
                
                try:
                    httpd.serve_forever()
                except KeyboardInterrupt:
                    print("\n🛑 Stopping server...")
                    self._running = False
                    httpd.shutdown()
        except OSError as e:
            print(f"❌ Failed to start server: {e}")
    
    def stop(self):
        """Stop the server"""
        if self._server:
            self._server.shutdown()
            self._running = False
    
    def is_running(self):
        return self._running


# Utility functions for responses
def json_response(data, status=200):
    """Create JSON response"""
    return Response().set_status(status).json(data)

def html_response(content, status=200):
    """Create HTML response"""
    return Response().set_status(status).html(content)

def text_response(content, status=200):
    """Create text response"""
    return Response().set_status(status).text(content)

def redirect_response(url, status=302):
    """Create redirect response"""
    return Response().set_status(status).redirect(url)

def file_response(content, filename, mime_type='application/octet-stream'):
    """Create file response"""
    return Response().file(content, filename, mime_type)

def error_response(message, status=400):
    """Create error response"""
    return Response().set_status(status).json({
        'error': True,
        'message': message
    })

# server.py - Add session support

def session_middleware(session_manager):
    """Middleware for session handling"""
    def middleware(request):
        # Get or create session
        response = request.get('_response')
        session = session_manager.get_session(request, response)
        request.session = session
        return None  # Continue to route
    return middleware

# Usage in NovaServer
# server.use(session_middleware(session_manager))