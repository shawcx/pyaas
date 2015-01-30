
class CacheTx(object):

    def __init__(self, mem, next=None):
        self._mem = mem
        self._next = next

    def __enter__(self):
        return self

    def __exit__(self):
        self.end()

    def put(self, key, field, value):
        self._mem.put(key, field, value)
        if self._next is not None:
            self._next.put(key, field, value)
        return self

    def remove(self, key, field):
        self._mem.remove(key, field)
        if self._next is not None:
            self._next.remove(key, field)
        return self

    def end(self):
        if self._next is not None:
            self._next.end()


class Memory(object):

    def __init__(self, next=None):
        self._l1 = {}
        self._next = next

    def start(self):
        if self._next is None:
            return CacheTx(self, None)
        return CacheTx(self, self._next.start())

    def put(self, key, field, value):
        if key not in self._l1:
            self._l1 = {}
        self._l1[key][field] = value
        if self._next is not None:
            self._next.put(key, field, value)

    def get(self, key, field):
        try:
            return self._l1[key][field]
        except KeyError:
            pass
        if self._next is not None:
            if key not in self._l1:
                self._l1 = {}
            obj = self._l1[key][field] = self._next.get(key, field)
            return obj
        return None

    def remove(self, key, field):
        try:
            del self._l1[key][field]
        except KeyError:
            pass
        if self._next is not None:
            self._next.remove(key, field)

    def removeall(self, key):
        try:
            del self._l1[key]
        except KeyError:
            pass
        if self._next is not None:
            self._next.removeall(key)

    def getall(self, key):
        if self._next is not None:
            return self._next.getall(key)
        else:
            try:
                return self._l1[key]
            except KeyError:
                pass
        return {}