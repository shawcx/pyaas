import sys
import logging

import pymongo
import gridfs
import bson
import bson.json_util

import pyaas

def connect():
    dbserver = pyaas.args.dbhost  or pyaas.config.get('mongo', 'server')
    dbname   = pyaas.args.dbname  or pyaas.config.get('mongo', 'database')
    store    = pyaas.args.dbstore or pyaas.config.get('mongo', 'store')

    try:
        pyaas.mongo = pymongo.Connection(dbserver)
    except pymongo.errors.AutoReconnect:
        raise pyaas.error('Could not connect to database')

    if pyaas.args.reset and pyaas.args.confirm:
        pyaas.mongo.drop_database(dbname)
        pyaas.mongo.drop_database(store)
        sys.exit(0)
    elif pyaas.args.reset:
        logging.error('Reset issued without confirmation')
        sys.exit(-1)

    pyaas.mongo.document_class = bson.SON

    pyaas.db = pyaas.mongo[dbname]
    pyaas.fs = gridfs.GridFS(pyaas.mongo[store])
