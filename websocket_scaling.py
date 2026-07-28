# websocket_scaling.py
# Scalable WebSocket with Redis Pub/Sub

import json
import redis
import threading
import asyncio

class ScalableWebSocketServer:
    """Scalable WebSocket server with Redis pub/sub"""
    
    def __init__(self, redis_url='redis://localhost:6379'):
        self.redis = redis.from_url(redis_url)
        self.pubsub = self.redis.pubsub()
        self.clients = {}
        self.channels = {}
        self._running = False
    
    async def handle_connection(self, websocket, path):
        """Handle WebSocket connection with pub/sub"""
        client_id = str(id(websocket))
        self.clients[client_id] = websocket
        
        # Subscribe to user's private channel
        channel = f"user:{client_id}"
        self.pubsub.subscribe(channel)
        
        # Start listening to Redis
        asyncio.create_task(self._listen_redis())
        
        try:
            async for message in websocket:
                data = json.loads(message)
                event = data.get('event')
                payload = data.get('data', {})
                
                # Handle different events
                if event == 'subscribe':
                    room = payload.get('room')
                    self._subscribe_to_room(client_id, room)
                elif event == 'publish':
                    room = payload.get('room')
                    self._publish_to_room(room, payload)
        
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            # Cleanup
            if client_id in self.clients:
                del self.clients[client_id]
            self.pubsub.unsubscribe(channel)
    
    async def _listen_redis(self):
        """Listen to Redis pub/sub messages"""
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                channel = message['channel']
                data = json.loads(message['data'])
                
                # Forward to appropriate clients
                if channel.startswith('room:'):
                    room = channel[5:]
                    if room in self.channels:
                        for client_id in self.channels[room]:
                            if client_id in self.clients:
                                await self.clients[client_id].send(json.dumps(data))
    
    def _subscribe_to_room(self, client_id, room):
        """Subscribe a client to a room"""
        if room not in self.channels:
            self.channels[room] = set()
            self.pubsub.subscribe(f"room:{room}")
        self.channels[room].add(client_id)
    
    def _publish_to_room(self, room, data):
        """Publish a message to a room"""
        self.redis.publish(f"room:{room}", json.dumps(data))