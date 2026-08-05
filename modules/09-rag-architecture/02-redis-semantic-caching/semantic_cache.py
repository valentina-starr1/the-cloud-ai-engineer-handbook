"""
semantic_cache.py

A lightweight semantic cache wrapper using Redis for vector similarity lookups.
If the similarity exceeds a configured threshold, return cached results; otherwise call the provided fallback retriever.
"""
import os
import numpy as np
import redis
import json
from typing import Callable, Any, List, Dict

REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
SIMILARITY_THRESHOLD = float(os.environ.get('SEMANTIC_CACHE_THRESHOLD', '0.85'))
CACHE_TTL = int(os.environ.get('SEMANTIC_CACHE_TTL', '3600'))

class SemanticCache:
    def __init__(self, redis_url: str = REDIS_URL):
        self.r = redis.from_url(redis_url)

    def _vec_to_bytes(self, vec: List[float]) -> bytes:
        return np.array(vec, dtype=np.float32).tobytes()

    def _bytes_to_vec(self, b: bytes) -> List[float]:
        return np.frombuffer(b, dtype=np.float32).tolist()

    def lookup(self, key: str, query_vec: List[float]) -> Dict[str, Any]:
        """
        Lookup cached nearest neighbor for the key. Returns dict with keys:
        - hit: bool
        - score: float
        - value: Any
        """
        entry = self.r.hgetall(key)
        if not entry:
            return {'hit': False}
        try:
            cached_vec = self._bytes_to_vec(entry[b'vec'])
            # cosine similarity
            q = np.array(query_vec, dtype=np.float32)
            c = np.array(cached_vec, dtype=np.float32)
            score = float(np.dot(q, c) / (np.linalg.norm(q) * np.linalg.norm(c) + 1e-12))
            if score >= SIMILARITY_THRESHOLD:
                value = json.loads(entry.get(b'value', b'null'))
                return {'hit': True, 'score': score, 'value': value}
        except Exception:
            return {'hit': False}
        return {'hit': False}

    def store(self, key: str, vec: List[float], value: Any):
        payload = {
            'vec': self._vec_to_bytes(vec),
            'value': json.dumps(value)
        }
        # Use a Redis hash to store binary vec and JSON value
        self.r.hset(key, mapping=payload)
        self.r.expire(key, CACHE_TTL)

    def get_or_compute(self, key: str, query_vec: List[float], fallback: Callable[[], Any]) -> Dict[str, Any]:
        res = self.lookup(key, query_vec)
        if res.get('hit'):
            return res
        value = fallback()
        # Optionally store embedding vector and value
        try:
            self.store(key, query_vec, value)
        except Exception:
            pass
        return {'hit': False, 'value': value}

# Usage example (replace with real embedding function and vector store)
if __name__ == '__main__':
    def fallback():
        return {'answer': 'computed'}

    cache = SemanticCache()
    qvec = [0.1, 0.2, 0.3, 0.4]
    print(cache.get_or_compute('query:example', qvec, fallback))
