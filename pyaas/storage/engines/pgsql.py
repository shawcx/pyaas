
import os

import pyaas

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    raise pyaas.error('Missing psycopg2 (Postgresql) module')


class Pgsql:
    def __init__(self, **kwds):
        self.schema = kwds.get('schema', None)
        if self.schema is not None:
            del kwds['schema']

        try:
            self.conn = psycopg2.connect(**kwds)
        except psycopg2.OperationalError as e:
            raise pyaas.error('Could not connect to database: %s', e)

        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def Initialize(self):
        if self.schema:
            schema = os.path.join(pyaas.prefix, self.schema)
            if schema and os.path.isfile(schema):
                with open(schema, 'rb') as f:
                    schema = f.read()
                    with self.conn as conn:
                        self.cursor.execute(schema)
                        conn.commit()

    def Sync(self):
        pass

    def Execute(self, statement, *args):
        with self.conn as conn:
            self.cursor.execute(statement, args)
            conn.commit()
        return self.cursor.fetchall()

    def Execute2(self, statement, *args):
        with self.conn as conn:
            self.cursor.execute(statement, args)
            conn.commit()

    def Find(self, table, params=None, sort=None):
        statement = 'SELECT * FROM ' + table
        if params:
            statement += ' WHERE ' + params
        if sort:
            statement += ''

        with self.conn as conn:
            self.cursor.execute(statement)
            conn.commit()

        return self.cursor.fetchall()

    def FindOne(self, table, _id, id_column='id'):
        statement = 'SELECT * FROM {0} WHERE {1} = %s'.format(table, id_column)
        with self.conn as conn:
            self.cursor.execute(statement, [_id])
            conn.commit()
        return self.cursor.fetchone()

    def Count(self, table):
        statement = 'SELECT count(*) FROM {0}'.format(table)
        with self.conn as conn:
            self.cursor.execute(statement)
            conn.commit()
        return self.cursor.fetchone()[0]

    def Insert(self, table, values, id_column='id'):
        columns = ','.join('"%s"' % k.lower() for k in values.keys())
        placeholder = ','.join('%s' for x in xrange(len(values)))
        statement = 'INSERT INTO {0} ({1}) VALUES ({2})'.format(table, columns, placeholder)

        with self.conn as conn:
            self.cursor.execute(statement, values.values())
            conn.commit()

        rows = self.cursor.rowcount
        if rows is None:
            rows = -1

        if id_column not in values:
            self.cursor.execute('SELECT lastval()')
            values[id_column] = self.cursor.fetchone()[0]

        return rows

    def Upsert(self, table, values, id_column='id'):
        rows = self.InsertUnique(table, values, id_column)
        if rows <= 0:
            rows = self.Update(table, values, id_column)
        return rows

    def InsertUnique(self, table, values, id_column='id'):
        columns = ','.join('"%s"' % k.lower() for k in values.keys())
        placeholder = ','.join('%s' for x in xrange(len(values)))
        statement = "INSERT INTO {0} ({1}) SELECT {2} WHERE NOT EXISTS (select {4} from {0} where {4} = '{3}')" \
            .format(table, columns, placeholder, values[id_column], id_column)

        with self.conn as conn:
            self.cursor.execute(statement, values.values())
            conn.commit()

        rows = self.cursor.rowcount
        if rows is None:
            rows = -1
        return rows

    def Update(self, table, values, id_column='id'):
        _id = values[id_column]
        columns = ','.join('"%s"=%%s' % s.lower() for s in values.keys())
        statement = 'UPDATE {0} SET {1} WHERE {2}=%s'.format(table, columns, id_column)

        with self.conn as conn:
            self.cursor.execute(statement, values.values() + [_id])
            conn.commit()

        rows = self.cursor.rowcount
        if rows is None:
            rows = -1
        return rows

    def Remove(self, table, _id, id_column='id'):
        statement = 'DELETE FROM {0} WHERE {1} = %s'.format(table, id_column)
        with self.conn as conn:
            self.cursor.execute(statement, [_id])
            conn.commit()
