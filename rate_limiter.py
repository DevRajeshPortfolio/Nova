# rate_limiter.py
# Distributed Rate Limiting for Nova

import time
import redis
from functools import wraps

class RateLimiter:
    """Distributed rate limiter using Redis"""
    
    def __init__(self, redis_client, window_seconds=60, max_requests=100):
        self.redis = redis_client
        self.window = window_seconds
        self.max_requests = max_requests
    
    def limit(self, key):
        """Check if request is allowed"""
        current = time.time()
        window_key = f"rate_limit:{key}:{int(current / self.window)}"
        
        count = self.redis.incr(window_key)
        if count == 1:
            self.redis.expire(window_key, self.window + 1)
        
        return count <= self.max_requests
    
    def limiter(self, key_func=None):
        """Decorator for rate limiting"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                key = key_func(*args, **kwargs) if key_func else 'default'
                if not self.limit(key):
                    raise Exception("Rate limit exceeded")
                return func(*args, **kwargs)
            return wrapper
        return decorator