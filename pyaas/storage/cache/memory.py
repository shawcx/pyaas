
class CacheTx(object):

    def __init__(self, l2):
        self._l2 = l2

    def __enter__(self):
        return self

    def __exit__(self):
        self._l2.__exit__()

    def put(self, key, field, value):
        self._l2.put(key, field, value)
        return self

    def remove(self, key, field):
        self._l2.remove(key, field)
        return self

    def end(self):
        self._l2.end()


class Memory(object):

    def __init__(self, l2):
        self._l1 = {}
        self._l2 = l2

    def start(self):
        return CacheTx(self._l2.start())

    def put(self, key, field, value):
        try:
            del self._l1[key][field]
        except KeyError:
            pass
        self._l2.put(key, field, value)

    def get(self, key, field):
        try:
            return self._l1[key][field]
        except KeyError:
            pass
        if key not in self._l1:
            self._l1 = {}
        obj = self._l1[key][field] = self._l2.get(key, field)
        return obj

    def remove(self, key, field):
        try:
            del self._l1[key][field]
        except KeyError:
            pass
        self._l2.remove(key, field)

    def removeall(self, key):
        try:
            del self._l1[key]
        except KeyError:
            pass
        self._l2.removeall(key)

    def getall(self, key):
        return self._l2.getall(key)