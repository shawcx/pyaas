import sys
import logging

import pyaas

try:
    import pymongo
    import gridfs
    import bson
    import motor
except ImportError:
    raise pyaas.error('Missing motor (mongodb) module')


class Mongo:
    def __init__(self, server, database, store=None):
        self.mongo = pymongo.Connection(server)
        self.motor = motor.MotorClient(server)

        self.mongo.document_class = bson.SON
        self.motor.document_class = bson.SON

        self.db  = self.mongo[database]
        self.mdb = self.motor[database]
        if store:
            self.fs  = gridfs.GridFS(self.mongo[store])
            self.mfs = motor.MotorGridFS(self.motor[store])
        else:
            self.fs  = None
            self.mfs = None

    def Initialize(self):
        return

    def Sync(self):
        return

    #def Reset(self):
    #    pyaas.mongo.drop_database(self.dbname)
    #    pyaas.mongo.drop_database(self.store)

    def Find(self, table, params=None, sort=None):
        return list(self.db[table].find(params, sort=sort))

    def FindOne(self, table, _id):
        return self.mongo[table].find_one(_id)

    def Count(self, table):
        return 0

    def Insert(self, table, values):
        return

    def Update(self, table, values=None):
        if values:
            self.record.update(values)
        self.db[table].save(self.record)
        return self

    def Remove(self, table, _id):
        self.db[table].remove(self.id)
        return True
