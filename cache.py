# cache.py
# Distributed Caching for Nova

import hashlib
import json
import time
from collections import OrderedDict

class Cache:
    """Multi-level caching system"""
    
    def __init__(self):
        self.memory_cache = MemoryCache()
        self.distributed_cache = None  # Redis, Memcached, etc.
    
    def get(self, key):
        """Get value from cache"""
        # Check memory cache first (L1)
        value = self.memory_cache.get(key)
        if value is not None:
            return value
        
        # Check distributed cache (L2)
        if self.distributed_cache:
            value = self.distributed_cache.get(key)
            if value is not None:
                self.memory_cache.set(key, value)
        
        return value
    
    def set(self, key, value, ttl=3600):
        """Set value in cache"""
        self.memory_cache.set(key, value, ttl)
        if self.distributed_cache:
            self.distributed_cache.set(key, value, ttl)

class MemoryCache:
    """In-memory cache with LRU eviction"""
    
    def __init__(self, max_size=1000):
        self.cache = OrderedDict()
        self.max_size = max_size
        self.ttl = {}
    
    def get(self, key):
        """Get value from cache"""
        if key in self.cache:
            # Check TTL
            if key in self.ttl and time.time() > self.ttl[key]:
                del self.cache[key]
                del self.ttl[key]
                return None
            # Move to end (LRU)
            self.cache.move_to_end(key)
            return self.cache[key]
        return None
    
    def set(self, key, value, ttl=3600):
        """Set value in cache"""
        if len(self.cache) >= self.max_size:
            # Remove oldest
            self.cache.popitem(last=False)
        self.cache[key] = value
        if ttl:
            self.ttl[key] = time.time() + ttl