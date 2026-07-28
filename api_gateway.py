# api_gateway.py
# API Gateway for Routing Requests

import json
import aiohttp
import asyncio
from urllib.parse import urljoin

class APIGateway:
    """API Gateway for Nova microservices"""
    
    def __init__(self, registry: ServiceRegistry):
        self.registry = registry
        self.routes = {}
        self.middleware = []
        self.session = None
    
    async def initialize(self):
        """Initialize the gateway"""
        self.session = aiohttp.ClientSession()
    
    def add_route(self, path: str, service_name: str):
        """Add a route to a service"""
        self.routes[path] = service_name
    
    def use(self, middleware):
        """Add global middleware"""
        self.middleware.append(middleware)
    
    async def handle_request(self, request):
        """Handle an incoming request"""
        # Find matching route
        path = request.path
        service_name = self._match_route(path)
        
        if not service_name:
            return self._error_response(404, "Route not found")
        
        # Get service instance
        instance = self.registry.get_instance(service_name)
        if not instance:
            return self._error_response(503, "Service unavailable")
        
        # Forward request
        try:
            url = f"http://{instance['host']}:{instance['port']}{path}"
            async with self.session.request(
                method=request.method,
                url=url,
                headers=request.headers,
                data=request.body
            ) as response:
                return {
                    'status': response.status,
                    'headers': dict(response.headers),
                    'body': await response.text()
                }
        except Exception as e:
            return self._error_response(500, str(e))
    
    def _match_route(self, path):
        """Match route to service"""
        # Exact match
        if path in self.routes:
            return self.routes[path]
        
        # Prefix match (longest prefix)
        matching = []
        for route, service in self.routes.items():
            if path.startswith(route):
                matching.append((len(route), service))
        
        if matching:
            matching.sort(reverse=True)
            return matching[0][1]
        
        return None
    
    def _error_response(self, status, message):
        """Create error response"""
        return {
            'status': status,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': message})
        }