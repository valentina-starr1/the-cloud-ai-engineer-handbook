# Redis Semantic Caching for LLMs

This module shows how to use Redis as a semantic cache to reduce vector similarity calls and LLM cost/latency. It assumes Redis with vector capabilities (RedisVector or Redis 7+ modules) is available.

Key ideas:

- Cache vector embeddings and nearest-neighbor results for repeated queries.
- Use a similarity threshold to decide when to return cache hits vs. re-run the full retrieval.
- Store metadata and TTLs to keep cache warm for common queries.

Files:
- redis.conf: example Redis configuration enabling vector module (adjust for your environment).
- semantic_cache.py: Python wrapper encapsulating cache lookup and fallback to the vector index.
