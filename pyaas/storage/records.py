
import json
import collections

import pyaas

__all__ = ['Records', 'Record']


class Records:
    def __init__(self, records):
        self.records = records

    @classmethod
    def Read(cls, params=None, sort=None):
        return cls(pyaas.db.Find(cls.RECORD.__name__, params, sort))

    def Delete(self):
        for record in self.records:
            self.RECORD(record).Delete()
        pass

    @classmethod
    def Count(cls):
        return pyaas.db.Count(cls.RECORD.__name__)

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
    def __init__(self, record):
        try:
            self.id = record['id']
        except KeyError:
            self.id = None
        self.record = dict(record)
        self.Init()

    def Init(self):
        pass

# CRUD methods

    @classmethod
    def Create(cls, values):
        return cls(values).Insert()

    def Insert(self):
        pyaas.db.Insert(self.__class__.__name__, self.record)
        if self.id is None:
            self.id = self.record['id']
        return self

    @classmethod
    def Read(cls, _id):
        record = pyaas.db.FindOne(cls.__name__, _id)
        return cls(record) if record else None

    def Update(self, values=None):
        if values:
            self.record.update(values)
        pyaas.db.Update(self.__class__.__name__, self.record)
        return self

    def Delete(self):
        pyaas.db.Remove(self.__class__.__name__, self.id)
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
