
import pyaas

try:
    import redis
except ImportError:
    raise pyaas.error('Missing redis module')


class CacheTx(object):

    def __init__(self, redis):
        self._pipeline = redis.pipeline()

    def __enter__(self):
        return self

    def __exit__(self):
        self.end()

    def put(self, key, field, value):
        self._pipeline.hset(key, field, value)
        return self

    def remove(self, key, field):
        self._pipeline.hdel(key, field)
        return self

    def end(self):
        self._pipeline.execute()


class Pyredis(object):

    def __init__(self, **kwargs):
        self._redis = redis.StrictRedis(**kwargs)

    def start(self):
        return CacheTx(self._redis)

    def put(self, key, field, value):
        self._redis.hset(key, field, value)

    def get(self, key, field):
        return self._redis.hget(key, field)

    def remove(self, key, field):
        self._redis.hdel(key, field)

    def removeall(self, key):
        self._redis.delete(key)

    def getall(self, key):
        return self._redis.hgetall(key)
