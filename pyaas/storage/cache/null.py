

class CacheTx(object):

    def __enter__(self):
        return self

    def __exit__(self):
        self.end()

    def put(self, key, field, value):
        raise NotImplementedError()

    def remove(self, key, field):
        raise NotImplementedError()

    def end(self):
        raise NotImplementedError()


class Cache(object):

    def start(self):
        raise NotImplementedError()

    def put(self, key, field, value):
        raise NotImplementedError()

    def get(self, key, field):
        raise NotImplementedError()

    def remove(self, key, field):
        raise NotImplementedError()

    def removeall(self, key):
        raise NotImplementedError()

    def getall(self, key):
        raise NotImplementedError()