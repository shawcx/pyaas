import sys
import logging

import pyaas

try:
    import pymongo
    import gridfs
    import bson
    import bson.json_util
except ImportError:
    raise pyaas.error('Missing pymongo module')


class Database:
    def __init__(self, **kwds):
        self.dbserver = pyaas.args.dbhost  or pyaas.config.get('mongo', 'server')
        self.dbname   = pyaas.args.dbname  or pyaas.config.get('mongo', 'database')
        self.store    = pyaas.args.dbstore or pyaas.config.get('mongo', 'store')

        try:
            pyaas.mongo = pymongo.Connection(self.dbserver)
        except pymongo.errors.AutoReconnect:
            raise pyaas.error('Could not connect to database')

        if pyaas.args.reset and pyaas.args.confirm:
            self.Reset()
            sys.exit(0)
        elif pyaas.args.reset:
            logging.error('Reset issued without confirmation')
            sys.exit(-1)

        pyaas.mongo.document_class = bson.SON

        pyaas.db = pyaas.mongo[self.dbname]
        pyaas.fs = gridfs.GridFS(pyaas.mongo[self.store])

    def Initialize(self):
        return

    def Reset(self):
        pyaas.mongo.drop_database(self.dbname)
        pyaas.mongo.drop_database(self.store)

    def Find(self, table, params=None, sort=None):
        return list(pyaas.db[table].find(params, sort=sort))

    def FindOne(self, table, _id):
        return pyaas.mongo[table].find_one(_id)

    def Count(self, table):
        return 0

    def Insert(self, table, values):
        return

    def Update(self, table, values=None):
        if values:
            self.record.update(values)
        pyaas.db[table].save(self.record)
        return self

    def Remove(self, table, _id):
        pyaas.db[table].remove(self.id)
        return True
