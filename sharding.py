# sharding.py
# Database Sharding for Horizontal Scaling

import hashlib

class ShardManager:
    """Database sharding manager"""
    
    def __init__(self, shards: List[str], shard_key: str = 'id'):
        self.shards = shards
        self.shard_key = shard_key
        self.shard_map = {}
        self._lock = threading.Lock()
    
    def get_shard(self, key_value):
        """Get shard for a given key"""
        if not self.shards:
            return None
        
        # Consistent hashing
        hash_value = self._hash_key(key_value)
        shard_index = hash_value % len(self.shards)
        return self.shards[shard_index]
    
    def _hash_key(self, key_value):
        """Hash a key value"""
        return int(hashlib.md5(str(key_value).encode()).hexdigest(), 16)
    
    def get_all_shards(self):
        """Get all shards"""
        return self.shards
    
    def add_shard(self, shard_url):
        """Add a new shard"""
        with self._lock:
            self.shards.append(shard_url)
    
    def remove_shard(self, shard_url):
        """Remove a shard"""
        with self._lock:
            if shard_url in self.shards:
                self.shards.remove(shard_url)