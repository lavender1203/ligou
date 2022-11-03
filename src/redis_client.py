from redis import ConnectionError, StrictRedis
from src.util import logger


class RedisClient:
    def __init__(self, redis_url, password=""):
        connection_kwargs = dict(
            socket_timeout=0.5, retry_on_timeout=True, socket_keepalive=True
        )
        connection_kwargs['password'] = password
        self.client = StrictRedis.from_url(
            redis_url, decode_responses=True, **connection_kwargs
        )
        self.raw_client = StrictRedis.from_url(redis_url, **connection_kwargs)
        logger.info(f'Initializing redis success.')
        self._detect_connectivity()

    def _detect_connectivity(self):
        self.client.ping()
