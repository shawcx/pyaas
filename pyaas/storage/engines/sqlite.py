
import os

import pyaas

try:
    import sqlite3
except ImportError:
    raise pyaas.error('Missing sqlite3 module')


class Database:
    def __init__(self, path=None, schema=None):
        if path is None:
            path = ':memory:'
        else:
            path = os.path.join(pyaas.prefix, path)
            # TODO: make any missing directories

        try:
            self.conn = sqlite3.connect(path)
        except sqlite3.OperationalError:
            raise pyaas.error('Unable to open database: %s', path)

        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.schema = schema

    def Initialize(self):
        if self.schema:
            schema = os.path.join(pyaas.prefix, self.schema)
            if schema and os.path.isfile(schema):
                schema = open(schema, 'rb').read()
                self.cursor.executescript(schema)
                self.conn.commit()

    def Find(self, table, params=None, sort=None):
        statement = 'SELECT * FROM ' + table
        if params:
            statement += ' WHERE ' + params
        if sort:
            statement += ''

        self.cursor.execute(statement)
        return self.cursor.fetchall()

    def FindOne(self, table, _id):
        statement = 'SELECT * FROM {0} WHERE id = ?'.format(table)
        self.cursor.execute(statement, [_id])
        return self.cursor.fetchone()

    def Count(self, table):
        statement = 'SELECT count(*) FROM {0}'.format(table)
        self.cursor.execute(statement)
        return self.cursor.fetchone()[0]

    def Insert(self, table, values, key='id'):
        columns = ','.join(values.keys())
        placeholder = ','.join('?' * len(values))
        statement = 'INSERT INTO {0} ({1}) VALUES ({2})'.format(table, columns, placeholder)

        try:
            self.cursor.execute(statement, values.values())
        except sqlite3.ProgrammingError:
            raise pyaas.error('Problem executing statement')

        if key not in values:
            values[key] = self.cursor.lastrowid

        self.conn.commit()

    def Update(self, table, values, key='id'):
        _id = values[key]
        columns = ','.join(s + '=?' for s in values.keys())
        statement = 'UPDATE {0} SET {1} WHERE id=?'.format(table, columns, _id)
        try:
            self.cursor.execute(statement, values.values() + [_id])
        except sqlite3.ProgrammingError:
            raise pyaas.error('Problem executing statement')

        self.conn.commit()

    def Remove(self, table, _id):
        statement = 'DELETE FROM {0} WHERE id = ?'.format(table)
        self.cursor.execute(statement, [_id])
        self.conn.commit()
