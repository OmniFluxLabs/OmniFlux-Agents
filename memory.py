import redis
import json
import os
from typing import Any, Optional
from datetime import timedelta


class RedisMemory:
    """Redis-based memory manager for shared context across agents."""
    
    def __init__(self, host: str = None, port: int = None):
        self.host = host or os.getenv("REDIS_HOST", "localhost")
        self.port = port or int(os.getenv("REDIS_PORT", 6379))
        self.client = None
        self._connect()
    
    def _connect(self):
        """Establish connection to Redis with retry logic."""
        try:
            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                decode_responses=True,
                socket_connect_timeout=5
            )
            self.client.ping()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Redis: {str(e)}")
    
    def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Store a value in Redis."""
        try:
            serialized = json.dumps(value)
            if ttl:
                return self.client.setex(key, timedelta(seconds=ttl), serialized)
            return self.client.set(key, serialized)
        except Exception as e:
            raise RuntimeError(f"Failed to set key {key}: {str(e)}")
    
    def get(self, key: str) -> Optional[Any]:
        """Retrieve a value from Redis."""
        try:
            value = self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            raise RuntimeError(f"Failed to get key {key}: {str(e)}")
    
    def delete(self, key: str) -> bool:
        """Delete a key from Redis."""
        try:
            return self.client.delete(key) > 0
        except Exception as e:
            raise RuntimeError(f"Failed to delete key {key}: {str(e)}")
    
    def exists(self, key: str) -> bool:
        """Check if a key exists."""
        try:
            return self.client.exists(key) > 0
        except Exception as e:
            raise RuntimeError(f"Failed to check key {key}: {str(e)}")
    
    def append_to_list(self, key: str, value: Any) -> int:
        """Append a value to a list."""
        try:
            serialized = json.dumps(value)
            return self.client.rpush(key, serialized)
        except Exception as e:
            raise RuntimeError(f"Failed to append to list {key}: {str(e)}")
    
    def get_list(self, key: str) -> list:
        """Get all values from a list."""
        try:
            values = self.client.lrange(key, 0, -1)
            return [json.loads(v) for v in values]
        except Exception as e:
            raise RuntimeError(f"Failed to get list {key}: {str(e)}")
    
    def clear_all(self) -> bool:
        """Clear all keys (use with caution)."""
        try:
            return self.client.flushdb()
        except Exception as e:
            raise RuntimeError(f"Failed to clear database: {str(e)}")
