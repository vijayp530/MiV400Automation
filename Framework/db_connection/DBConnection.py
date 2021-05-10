"""
This module provides connection to the different data bases
"""
__author__ = "nitin.kumar-2@mitel.com"

import logging

log = logging.getLogger("DBConnection.db")
log.addHandler(logging.NullHandler())


class DBConnection:

    def __init__(self, db_type='mssql'):
        """
        :param db_type: the type of db to connect to i.e. possible values are ['mssql', 'mysql']
        """
        ALL_DB_TYPES = ['mssql', 'mysql', 'postgres']
        self.db_type = db_type
        self.connection = None
        if self.db_type not in ALL_DB_TYPES:
            raise Exception("Requesting connection to <%s> DB.db_type should be one of %s" % (self.db_type, ALL_DB_TYPES))

    def connect(self, hostname, port, username, password, dbname, **kwargs):
        """
        connects to a db based on passed credential
        :param hostname: the ip of server
        :param port: port number
        :param username: username
        :param password: password
        :param dbname: the name of data base
        :param kwargs: optional keyword args
        :return: None
        """
        if self.db_type == 'mssql':
            import pymssql
            _connect = getattr(pymssql, 'connect')
        elif self.db_type == 'mysql':
            import pymysql
            _connect = getattr(pymysql, 'connect')
        elif self.db_type == 'postgres':
            import psycopg2
            _connect = getattr(psycopg2, 'connect')
        self.connection = _connect(host=hostname, port=port, user=username, password=password, database=dbname, **kwargs)

    def execute_query(self, query, result_as_dict=True):
        """
        creates a cursor and executes a given query
        :param query: the sql query to be executed
        :param result_as_dict: True if result is desired in dictionary format i.e. coloumn name with value
        :return: list of rows
        """
        if result_as_dict:
            if self.db_type == 'mssql':
                cursor = self.connection.cursor(as_dict=True)
            elif self.db_type == 'mysql':
                from pymysql.cursors import DictCursor
                cursor = self.connection.cursor(DictCursor)
            elif self.db_type == 'postgres':
                import psycopg2.extras
                cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        else:
            cursor = self.connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        if len(rows) == 0:
            log.debug("last query <%s> returned 0 result" % query)
        if type(rows[0]) in [dict,list,tuple]:
            return rows
        else:
            _rows = []
            for row in rows:
                _rows.append(dict(row))
            return _rows



if __name__ == "__main__":
    d = True
    # UC db
    x1 = DBConnection('postgres')
    x1.connect(hostname='localhost',username='postgres',password='1234',port=5432,dbname='dvdrental')
    print((x1.execute_query("SELECT * FROM actor ORDER BY first_name LIMIT 10", result_as_dict=d)))

    # boss db
    x1 = DBConnection('mssql')
    x1.connect(hostname='10.196.7.182',username='m5portal',password='1234',port=1433,dbname='m5db')
    print((x1.execute_query("SELECT TOP 3 * FROM person", result_as_dict=d)))

    # d2 db
    x2 = DBConnection('mysql')
    x2.connect(hostname='10.197.145.186', username='shoreadmin', password='passwordshoreadmin', port=4308, dbname='shoreware')
    print(x2.execute_query("SELECT * FROM users LIMIT 1", result_as_dict=d))
