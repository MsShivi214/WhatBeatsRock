import redis
import json
from typing import Optional
import os

class CacheManager:
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.redis_client = redis.from_url(self.redis_url)
        
    def get_cached_verdict(self, word_pair: str) -> Optional[bool]:
        """Get cached AI verdict for a word pair"""
        cached = self.redis_client.get(f"verdict:{word_pair}")
        if cached:
            return json.loads(cached)
        return None
        
    def cache_verdict(self, word_pair: str, verdict: bool, ttl: int = 3600):
        """Cache AI verdict for a word pair with TTL"""
        self.redis_client.setex(
            f"verdict:{word_pair}",
            ttl,
            json.dumps(verdict)
        )
        
    def increment_global_guess(self, word: str) -> int:
        """Increment and get the global guess count for a word"""
        return self.redis_client.incr(f"global_guess:{word}")
        
    def get_global_guess_count(self, word: str) -> int:
        """Get the global guess count for a word"""
        count = self.redis_client.get(f"global_guess:{word}")
        return int(count) if count else 0
        
    def check_rate_limit(self, ip: str) -> bool:
        """Check if an IP has exceeded the rate limit"""
        key = f"rate_limit:{ip}"
        current = self.redis_client.incr(key)
        if current == 1:
            self.redis_client.expire(key, 60)  # Reset after 1 minute
        return current <= int(os.getenv("RATE_LIMIT_PER_MINUTE", 100))

# Create a singleton instance
cache_manager = CacheManager() 