
import pyaas


def cache_record_result(func):
    def _record_result(*args, **kwargs):

        # check cache
        if pyaas.cache:
            k = 'Cache:Record:' + args[1]
            r = pyaas.cache.get(k, args[2])
            if r is not None:
                return r

        r = func(*args, **kwargs)

        # cache it
        if pyaas.cache:
            pyaas.cache.put(k, args[2], r)

        return r
    return _record_result

def cache_record_remove(func):
    def _record_remove(*args, **kwargs):
        r = func(*args, **kwargs)

        # drop it
        if pyaas.cache:
            k = 'Cache:Record:' + args[1]
            pyaas.cache.remove(k, args[2][args[3]])

        return r

    return _record_remove

def cache_result(func):
    def _result(*args, **kwargs):

        # check cache
        if pyaas.cache:
            k = 'Cache:Result:' + args[1]
            r = pyaas.cache.get(k, 'result')
            if r is not None:
                return r

        r = func(*args, **kwargs)

        # cache it
        if pyaas.cache:
            pyaas.cache.put(k, 'result', r)

        return r

    return _result


def cache_remove(func, key):
    def _remove(*args, **kwargs):

        r = func(*args, **kwargs)

        if pyaas.cache:
            pyaas.cache.remove(key, '__field')

        return r
    return _remove