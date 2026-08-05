"""
Redis-backed token bucket limiter for Python.
This implementation uses Redis atomic operations via EVAL (Lua) for correctness.
"""
import time
import redis

TOKEN_BUCKET_LUA = '''
local key = KEYS[1]
local rate = tonumber(ARGV[1])
local capacity = tonumber(ARGV[2])
local now = tonumber(ARGV[3])
local requested = tonumber(ARGV[4])

local token_info = redis.call('HMGET', key, 'tokens', 'last')
local tokens = tonumber(token_info[1]) or capacity
local last = tonumber(token_info[2]) or 0

local delta = math.max(0, now - last)
local add = delta * rate
tokens = math.min(capacity, tokens + add)

local allowed = 0
if tokens >= requested then
  tokens = tokens - requested
  allowed = 1
end

redis.call('HMSET', key, 'tokens', tokens, 'last', now)
redis.call('EXPIRE', key, 3600)
return allowed
'''

class TokenBucketLimiter:
    def __init__(self, redis_url='redis://localhost:6379/0'):
        self.r = redis.Redis.from_url(redis_url)

    def allow(self, key: str, rate: float, capacity: float, requested: float = 1.0) -> bool:
        now = time.time()
        allowed = self.r.eval(TOKEN_BUCKET_LUA, 1, key, rate, capacity, now, requested)
        return bool(allowed)

if __name__ == '__main__':
    tb = TokenBucketLimiter()
    k = 'token_bucket:client:example'
    allowed = tb.allow(k, rate=1.0, capacity=5.0)
    print('allowed', allowed)
