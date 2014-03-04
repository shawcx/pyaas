
import json
import UserDict

import pyaas

__all__ = ['Records', 'Record']

class Records:
    def __init__(self, entries):
        self.entries = entries

    @classmethod
    def Read(cls, params=None, sort=None):
        return cls(pyaas.db.Find(cls.ENTRY.__name__, params, sort))

    def Delete(self):
        for entry in self.entries:
            self.ENTRY(entry).Delete()
        pass

    @classmethod
    def Count(cls):
        return pyaas.db.Count(cls.ENTRY.__name__)

# List methods to iterate over the collection

    def __len__(self):
        return len(self.entries)

    def __iter__(self):
        for entry in self.entries:
            yield self.ENTRY(entry)

    def __getitem__(self, idx):
        return self.entries.__getitem__(idx)

    @property
    def json(self):
        return json.dumps([dict(e) for e in self.entries], separators=(',',':'))



class Record(object, UserDict.DictMixin):
    def __init__(self, entry):
        try:
            self.id = entry['id']
        except KeyError:
            self.id = None
        self.entry = dict(entry)
        self.Init()

    def Init(self):
        pass

# CRUD methods

    @classmethod
    def Create(cls, values):
        return cls(values).Insert()

    def Insert(self):
        pyaas.db.Insert(self.__class__.__name__, self.entry)
        if self.id is None:
            self.id = self.entry['id']
        return self

    @classmethod
    def Read(cls, _id):
        entry = pyaas.db.FindOne(cls.__name__, _id)
        return cls(entry) if entry else None

    def Update(self, values=None):
        if values:
            self.entry.update(values)
        pyaas.db.Update(self.__class__.__name__, self.entry)
        return self

    def Delete(self):
        pyaas.db.Remove(self.__class__.__name__, self.id)
        return True

# Convenience function to access data as JSON

    @property
    def json(self):
        return json.dumps(dict(self.entry), separators=(',',':'))

# Direct access of entries

    def __getattr__(self, attr):
        try:
            return object.__getattribute__(self, attr)
        except AttributeError:
            if attr in self.entry:
                return self.entry[attr]
            raise

# Dictionary methods to access the data

    def __getitem__(self, key):
        return self.entry.__getitem__(key)

    def __setitem__(self, key, value):
        return self.entry.__setitem__(key, value)

    def __delitem__(self, key):
        return self.entry.__delitem__(key)

    def keys(self):
        return self.entry.keys()
