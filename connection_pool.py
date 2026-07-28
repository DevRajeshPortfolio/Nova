# connection_pool.py
# Database Connection Pooling for High Throughput

import threading
import queue
import time
from contextlib import contextmanager

class ConnectionPool:
    """Thread-safe connection pool for database connections"""
    
    def __init__(self, create_connection, max_connections=50, min_connections=5):
        self.create_connection = create_connection
        self.max_connections = max_connections
        self.min_connections = min_connections
        self._pool = queue.Queue()
        self._active = set()
        self._lock = threading.Lock()
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Initialize the pool with minimum connections"""
        for _ in range(self.min_connections):
            conn = self.create_connection()
            self._pool.put(conn)
    
    @contextmanager
    def get_connection(self):
        """Get a connection from the pool"""
        conn = self._pool.get()
        self._active.add(conn)
        try:
            yield conn
        finally:
            self._active.remove(conn)
            self._pool.put(conn)
    
    def close_all(self):
        """Close all connections"""
        while not self._pool.empty():
            conn = self._pool.get()
            conn.close()
        for conn in self._active:
            conn.close()