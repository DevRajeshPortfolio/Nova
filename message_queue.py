# message_queue.py
# Message Queue for Data Processing

import json
import threading
import time
from collections import deque

class MessageQueue:
    """In-memory message queue for data processing"""
    
    def __init__(self):
        self.queues = {}
        self.consumers = {}
        self._lock = threading.Lock()
        self._running = False
    
    def create_queue(self, name: str):
        """Create a new queue"""
        with self._lock:
            if name not in self.queues:
                self.queues[name] = deque()
                self.consumers[name] = []
    
    def publish(self, queue_name: str, message: Any):
        """Publish a message to a queue"""
        with self._lock:
            if queue_name not in self.queues:
                self.create_queue(queue_name)
            self.queues[queue_name].append(message)
            
            # Notify consumers
            self._notify_consumers(queue_name)
    
    def subscribe(self, queue_name: str, callback: Callable):
        """Subscribe to a queue"""
        with self._lock:
            if queue_name not in self.consumers:
                self.consumers[queue_name] = []
            self.consumers[queue_name].append(callback)
    
    def _notify_consumers(self, queue_name: str):
        """Notify consumers of new messages"""
        if queue_name in self.consumers:
            for consumer in self.consumers[queue_name]:
                try:
                    while self.queues[queue_name]:
                        message = self.queues[queue_name].popleft()
                        consumer(message)
                except Exception as e:
                    print(f"Consumer error: {e}")