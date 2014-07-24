
import os

import pyaas

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    raise pyaas.error('Missing psycopg2 module')


class Database:
    def __init__(self, **kwds):
        try:
            self.conn = psycopg2.connect(**kwds)
        except psycopg2.OperationalError as e:
            raise pyaas.error('Could not connect to database: %s', e)

        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def Initialize(self):
        schema = os.path.join(pyaas.prefix, pyaas.config.get('storage', 'schema'))
        schema = open(schema, 'rb').read()
        self.cursor.execute(schema)
        self.conn.commit()

    def Execute(self, statement, *args):
        try:
            self.cursor.execute(statement, args)
        except Exception as e:
            raise pyaas.error('Exception: %s', e)

        return self.cursor.fetchall()

    def Execute2(self, statement, *args):
        try:
            self.cursor.execute(statement, args)
            self.conn.commit()
        except Exception as e:
            raise pyaas.error('Exception: %s', e)

    def Find(self, table, params=None, sort=None):
        statement = 'SELECT * FROM ' + table
        if params:
            statement += ' WHERE ' + params
        if sort:
            statement += ''

        try:
            self.cursor.execute(statement)
        except psycopg2.ProgrammingError as e:
            raise pyaas.error('Error in statement: %s', e)

        return self.cursor.fetchall()

    def FindOne(self, table, _id):
        statement = 'SELECT * FROM {0} WHERE id = %s'.format(table)
        self.cursor.execute(statement, [_id])
        return self.cursor.fetchone()

    def Count(self, table):
        statement = 'SELECT count(*) FROM {0}'.format(table)
        self.cursor.execute(statement)
        return self.cursor.fetchone()[0]

    def Insert(self, table, values):
        columns = ','.join('"%s"' % k.lower() for k in values.keys())
        placeholder = ','.join('%s' for x in xrange(len(values)))
        statement = 'INSERT INTO {0} ({1}) VALUES ({2})'.format(table, columns, placeholder)

        try:
            self.cursor.execute(statement, values.values())
        except psycopg2.IntegrityError:
            self.conn.rollback()
        except psycopg2.ProgrammingError as e:
            raise pyaas.error('Postgres Programming Error: %s', e)
        else:
            self.conn.commit()
        rows = self.cursor.rowcount
        if rows is None:
            rows = -1
        return rows

    def InsertUnique(self, table, values):
        columns = ','.join('"%s"' % k.lower() for k in values.keys())
        placeholder = ','.join('%s' for x in xrange(len(values)))
        statement = "INSERT INTO {0} ({1}) SELECT {2} WHERE NOT EXISTS (select id from {0} where id = '{3}')" \
            .format(table, columns, placeholder, values['id'])

        try:
            self.cursor.execute(statement, values.values())
        except psycopg2.IntegrityError:
            self.conn.rollback()
        except psycopg2.ProgrammingError as e:
            raise pyaas.error('Postgres Programming Error: %s', e)
        else:
            self.conn.commit()
        rows = self.cursor.rowcount
        if rows is None:
            rows = -1
        return rows

    def Update(self, table, values):
        _id = values['id']
        columns = ','.join('"%s"=%%s' % s.lower() for s in values.keys())
        statement = 'UPDATE {0} SET {1} WHERE id=%s'.format(table, columns)
        try:
            self.cursor.execute(statement, values.values() + [_id])
        except psycopg2.ProgrammingError:
            raise
        self.conn.commit()
        rows = self.cursor.rowcount
        if rows is None:
            rows = -1
        return rows

    def Remove(self, table, _id):
        statement = 'DELETE FROM {0} WHERE id = %s'.format(table)
        self.cursor.execute(statement, [_id])
        self.conn.commit()
