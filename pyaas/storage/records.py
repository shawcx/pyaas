
import json
import collections
import abc

import pyaas

__all__ = ['Records', 'Record']

class Instance(type):
    def __getattr__(cls, key):
        try:
            return object.__getattribute__(cls, key)
        except AttributeError:
            try:
                cls.instance = pyaas.storage.databases[key]
                return cls
            except KeyError:
                raise AttributeError(key)

    def __getitem__(cls, key):
        # TODO: set instance to an actual database class instance
        try:
            cls.instance = pyaas.storage.databases[key]
            return cls
        except KeyError:
            raise AttributeError(key)

#    @property
#    def instance(self):
#        return self.instance
#
#    @instance.setter
#    def instance(self, value):
#        self.instance = value


class AbstractIntsance(Instance, abc.ABCMeta):
    'combined metaclass to support MutableMapping'


class Records(object):
    __metaclass__ = Instance

    def __init__(self, records):
        self.instance = self.__class__.instance
        self.records = records

    @classmethod
    def Read(cls, params=None, sort=None):
        return cls(cls.instance.Find(cls.RECORD.table(), params, sort))

    def Delete(self):
        for record in self.records:
            self.RECORD(record).Delete()
        pass

    @classmethod
    def Count(cls):
        return cls.instance.Count(cls.RECORD.table())

# List methods to iterate over the collection

    def __len__(self):
        return len(self.records)

    def __iter__(self):
        for record in self.records:
            yield self.RECORD(record)

    def __getitem__(self, idx):
        return self.records.__getitem__(idx)

    @property
    def json(self):
        return json.dumps([dict(e) for e in self.records], separators=(',', ':'))


class Record(collections.MutableMapping):
    __metaclass__ = AbstractIntsance

    TABLE_NAME = None
    ID_COLUMN = 'id'

    def __init__(self, record):
        self.instance = self.__class__.instance

        try:
            self.id = record[self.ID_COLUMN]
        except KeyError:
            self.id = None

        self.record = dict(record)
        self.Init()

    def Init(self):
        pass

    @classmethod
    def table(cls):
        return cls.__name__ if cls.TABLE_NAME is None else cls.TABLE_NAME

# CRUD methods

    @classmethod
    def Create(cls, values):
        return cls(values).Insert()

    def Insert(self):
        self.instance.Insert(self.table(), self.record)
        if self.id is None:
            self.id = self.record[self.ID_COLUMN]
        return self

    @classmethod
    def Read(cls, _id):
        record = cls.instance.FindOne(cls.table(), _id, cls.ID_COLUMN)
        return cls(record) if record else None

    def Update(self, values=None):
        if values:
            self.record.update(values)
        self.instance.Update(self.table(), self.record, self.ID_COLUMN)
        return self

    def Delete(self):
        self.instance.Remove(self.table(), self.id, self.ID_COLUMN)
        return True

# Convenience function to access data as JSON

    @property
    def json(self):
        return json.dumps(dict(self.record), separators=(',', ':'))

# Direct access of records

    def __getattr__(self, attr):
        try:
            return object.__getattribute__(self, attr)
        except AttributeError:
            if attr in self.record:
                return self.record[attr]
            raise

    def __iter__(self):
        return self.record.__iter__

    def __len__(self):
        return len(self.record)

# Dictionary methods to access the data

    def __getitem__(self, key):
        return self.record.__getitem__(key)

    def __setitem__(self, key, value):
        return self.record.__setitem__(key, value)

    def __delitem__(self, key):
        return self.record.__delitem__(key)

    def keys(self):
        return self.record.keys()
