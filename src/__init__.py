from .redis_client import RedisClient

__all__ = ['RedisClient']

redis = RedisClient(redis_url="redis://127.0.0.1:6379/1")
