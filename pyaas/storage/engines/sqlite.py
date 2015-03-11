
import os

import pyaas
import logging

try:
    import sqlite3
except ImportError:
    raise pyaas.error('Missing sqlite3 module')


class Sqlite:
    def __init__(self, path=None, schema=None):
        if path is None:
            path = ':memory:'
        else:
            path = pyaas.paths('var', path)
            # TODO: make any missing directories

        self.path = path
        self.schema = schema


    def Initialize(self):
        # Check if the db exists before we make a connection.  The connection
        # will create the file but it will not yet have a schema.
        exists = os.path.isfile(self.path)

        try:
            self.conn = sqlite3.connect(self.path)
            self.conn.text_factory = str
            self.conn.row_factory  = sqlite3.Row
            self.cursor = self.conn.cursor()
        except sqlite3.OperationalError:
            raise pyaas.error('Unable to open database: %s', self.path)

        if self.schema and not exists:
            schema = self.schema

            # Attempt to find the schema.  This is kind of dumb but it
            # prevents some old code from breaking.  At some point we
            # might could remove this first condition
            if not os.path.isfile(schema):
                schema = os.path.join(pyaas.prefix, self.schema)
            if not os.path.isfile(schema):
                schema = pyaas.paths('etc', self.schema)

            if os.path.isfile(schema):
                logging.debug('Attempt to load schema: %s', schema)
                schema = open(schema, 'rb').read()
                self.cursor.executescript(schema)
                self.conn.commit()
            else:
                logging.debug('Schema not found: %s', schema)

    def Cursor(self):
        return self.conn.cursor()

    def Close(self):
        self.conn.commit()
        self.conn.close()

    def Sync(self):
        self.conn.commit()

    def Find(self, table, params=None, sort=None):
        statement = 'SELECT * FROM ' + table
        if params:
            statement += ' WHERE ' + params
        if sort:
            statement += ' ' + sort

        self.cursor.execute(statement)
        return self.cursor.fetchall()

    def FindOne(self, table, _id, id_column='id'):
        statement = 'SELECT * FROM {0} WHERE {1} = ?'.format(table, id_column)
        self.cursor.execute(statement, [_id])
        return self.cursor.fetchone()

    def Count(self, table):
        statement = 'SELECT count(*) FROM {0}'.format(table)
        self.cursor.execute(statement)
        return self.cursor.fetchone()[0]

    def Insert(self, table, values, id_column='id'):
        columns = ','.join(values.keys())
        placeholder = ','.join('?' * len(values))
        statement = 'INSERT INTO {0} ({1}) VALUES ({2})'.format(table, columns, placeholder)

        try:
            self.cursor.execute(statement, values.values())
        except sqlite3.ProgrammingError as e:
            raise pyaas.error('Problem executing statement: %s', e)
        except sqlite3.IntegrityError as e:
            raise pyaas.error('Integrity error: %s', e)

        if id_column not in values:
            values[id_column] = self.cursor.lastrowid

        #self.conn.commit()

    def Update(self, table, values, id_column='id'):
        _id = values[id_column]
        columns = ','.join(s + '=?' for s in values.keys())
        statement = 'UPDATE {0} SET {1} WHERE id=?'.format(table, columns, _id)
        try:
            self.cursor.execute(statement, values.values() + [_id])
        except sqlite3.ProgrammingError:
            raise pyaas.error('Problem executing statement')

        #self.conn.commit()

    def Remove(self, table, _id, id_column='id'):
        statement = 'DELETE FROM {0} WHERE {1} = ?'.format(table, id_column)
        self.cursor.execute(statement, [_id])
        #self.conn.commit()
