# websocket.py
# Nova Programming Language - WebSocket Support

import json
import asyncio
import websockets
import threading
from datetime import datetime

class WebSocketServer:
    """WebSocket server for real-time communication"""
    
    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.clients = {}
        self.event_handlers = {}
        self._server = None
        self._running = False
        self._loop = None
        self._thread = None
    
    def on(self, event, handler):
        """Register event handler"""
        if event not in self.event_handlers:
            self.event_handlers[event] = []
        self.event_handlers[event].append(handler)
    
    def emit(self, event, data, client_id=None):
        """Emit event to client(s)"""
        message = json.dumps({
            'event': event,
            'data': data,
            'timestamp': datetime.now().isoformat()
        })
        
        if client_id and client_id in self.clients:
            # Send to specific client
            asyncio.run_coroutine_threadsafe(
                self.clients[client_id].send(message),
                self._loop
            )
        else:
            # Broadcast to all clients
            for client in self.clients.values():
                asyncio.run_coroutine_threadsafe(
                    client.send(message),
                    self._loop
                )
    
    def broadcast(self, data):
        """Broadcast data to all clients"""
        self.emit('broadcast', data)
    
    def start(self, host=None, port=None):
        """Start WebSocket server in background thread"""
        if host is not None:
            self.host = host
        if port is not None:
            self.port = port
        
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(
            target=self._run_server,
            daemon=True
        )
        self._thread.start()
        print(f"🔌 WebSocket server running at ws://{self.host}:{self.port}")
    
    def _run_server(self):
        """Run the server in a thread"""
        asyncio.set_event_loop(self._loop)
        start_server = websockets.serve(self._handler, self.host, self.port)
        
        self._server = self._loop.run_until_complete(start_server)
        self._running = True
        
        try:
            self._loop.run_forever()
        except KeyboardInterrupt:
            self.stop()
    
    async def _handler(self, websocket, path):
        """Handle WebSocket connection"""
        client_id = str(id(websocket))
        self.clients[client_id] = websocket
        
        # Trigger connection event
        self._trigger_event('connection', {'client_id': client_id})
        
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    event = data.get('event', 'message')
                    payload = data.get('data', {})
                    
                    # Trigger event handler
                    self._trigger_event(event, {
                        'client_id': client_id,
                        'data': payload
                    })
                    
                except json.JSONDecodeError:
                    # Handle plain text message
                    self._trigger_event('message', {
                        'client_id': client_id,
                        'data': message
                    })
                    
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            # Clean up
            if client_id in self.clients:
                del self.clients[client_id]
            
            # Trigger disconnection event
            self._trigger_event('disconnection', {'client_id': client_id})
    
    def _trigger_event(self, event, data):
        """Trigger event handlers"""
        if event in self.event_handlers:
            for handler in self.event_handlers[event]:
                try:
                    handler(data)
                except Exception as e:
                    print(f"Error in event handler: {e}")
    
    def stop(self):
        """Stop the server"""
        self._running = False
        if self._server:
            self._server.close()
            self._loop.run_until_complete(self._server.wait_closed())
        self._loop.stop()
        print("🔌 WebSocket server stopped")
    
    def get_client_count(self):
        """Get number of connected clients"""
        return len(self.clients)
    
    def get_clients(self):
        """Get list of connected client IDs"""
        return list(self.clients.keys())


class WebSocketClient:
    """WebSocket client for connecting to servers"""
    
    def __init__(self, url):
        self.url = url
        self.websocket = None
        self.event_handlers = {}
        self._running = False
    
    def on(self, event, handler):
        """Register event handler"""
        if event not in self.event_handlers:
            self.event_handlers[event] = []
        self.event_handlers[event].append(handler)
    
    async def connect(self):
        """Connect to WebSocket server"""
        try:
            self.websocket = await websockets.connect(self.url)
            self._running = True
            
            # Trigger connection event
            self._trigger_event('connection', {})
            
            # Start message loop
            asyncio.create_task(self._message_loop())
            return True
        except Exception as e:
            print(f"WebSocket connection error: {e}")
            return False
    
    async def _message_loop(self):
        """Message receiving loop"""
        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    event = data.get('event', 'message')
                    payload = data.get('data', {})
                    self._trigger_event(event, payload)
                except json.JSONDecodeError:
                    self._trigger_event('message', message)
        except websockets.exceptions.ConnectionClosed:
            self._running = False
            self._trigger_event('disconnection', {})
    
    def emit(self, event, data):
        """Emit event to server"""
        if self.websocket:
            message = json.dumps({'event': event, 'data': data})
            asyncio.run_coroutine_threadsafe(
                self.websocket.send(message),
                asyncio.get_event_loop()
            )
    
    def disconnect(self):
        """Disconnect from server"""
        self._running = False
        if self.websocket:
            asyncio.run_coroutine_threadsafe(
                self.websocket.close(),
                asyncio.get_event_loop()
            )
    
    def _trigger_event(self, event, data):
        """Trigger event handlers"""
        if event in self.event_handlers:
            for handler in self.event_handlers[event]:
                try:
                    handler(data)
                except Exception as e:
                    print(f"Error in event handler: {e}")


# Helper functions
def create_chat_room():
    """Create a simple chat room"""
    room = {
        'clients': [],
        'messages': [],
        'max_messages': 100
    }
    
    def broadcast(message, sender=None):
        """Broadcast message to all clients"""
        room['messages'].append({
            'sender': sender,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last N messages
        if len(room['messages']) > room['max_messages']:
            room['messages'] = room['messages'][-room['max_messages']:]
    
    def add_client(client_id):
        """Add a client to the room"""
        if client_id not in room['clients']:
            room['clients'].append(client_id)
            broadcast(f"User {client_id} joined the chat", 'system')
    
    def remove_client(client_id):
        """Remove a client from the room"""
        if client_id in room['clients']:
            room['clients'].remove(client_id)
            broadcast(f"User {client_id} left the chat", 'system')
    
    def get_messages(limit=50):
        """Get recent messages"""
        return room['messages'][-limit:]
    
    return {
        'broadcast': broadcast,
        'add_client': add_client,
        'remove_client': remove_client,
        'get_messages': get_messages,
        'clients': room['clients'],
        'messages': room['messages']
    }