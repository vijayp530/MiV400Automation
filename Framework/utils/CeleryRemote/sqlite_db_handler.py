###############################################################################
## Module         :    SQLiteDBHandler
## File name      :    sqlite_db_handler.py
## Description    :    This class contains methods related to operations on
##                     SQLite Database
##
## -----------------------------------------------------------------------
## Modification log:
##
## Date        Engineer              Description
## ---------   ---------      -----------------------
## 05 OCT 2015  UKumar             Initial Version
###############################################################################

import sqlite3


class SQLiteDBHandler(object):
    '''
    This class contains methods related to operations on SQLite Database
    '''

    #def __init__(self, logger):
    def __init__(self, logger):
        '''
        Constructor
        '''
        self.logger = logger

    def create_connection(self, dbPath):
        """ Creates connection to the database
        """
        try:
            self.logger.debug('Begin')
            self.db_connection = sqlite3.connect(dbPath)
            if self.db_connection:
                self.logger.info("connection established")
                self.db_cursor = self.db_connection.cursor()
                self.logger.info("Cursor Created")
            self.logger.debug('End')
        except sqlite3.DatabaseError as e:
            self.logger.error("Error in connection establishment!")
            raise e
    
    def get_cursor(self):
        """ Returns cursor of database connection
        """
        return self.db_cursor
        
    def execute_query(self, query, dataValues=''):
        """ Executes query
        """
        try:
            self.logger.debug('Begin')
            self.get_cursor().execute(query, dataValues)
            self.logger.debug('End')
        except sqlite3.DatabaseError as e:
            self.logger.error("Error in executing query!")
            raise e
        
    def insert_query(self, tableName, valuesTuple):
        """
        Takes table name and data values to insert as an argument, creates insert query
        and inserts the data to specified table
        """
        try:
            self.logger.debug('Begin')
            queryString = 'INSERT INTO '+tableName+' VALUES ('
            for i in range(0, len(valuesTuple)):
                queryString = queryString+'?,'
                
            queryString = queryString.rstrip(',')+')'
            self.logger.debug(queryString)
            self.execute_query(queryString, valuesTuple)
            self.db_connection.commit()
            self.logger.info("Changes Committed.")
            self.logger.debug('End')
        except sqlite3.DatabaseError as e:
            self.logger.error("Error in executing INSERT query!")
            raise e
        
    def select_query(self, query):
        """ Selects data from given table
        """
        try:
            self.logger.debug('Begin')
            self.execute_query(query)
            result = self.get_cursor().fetchall()
            self.logger.debug(result)
            self.logger.debug('End')
            return result
        except sqlite3.DatabaseError as e:
            self.logger.error("Error in executing SELECT query!")
            raise e
        
    #===========================================================================
    # def select_query(self, tableName, tupleIdentifier, columnName='*'):
    #     """ Selects data from given table
    #     """        
    #     if len(tupleIdentifier) == 0:
    #         query = self.select_query_without_where_clause(tableName, tupleIdentifier, columnName)
    #         #self.logger.debug(query)
    #     else:
    #         query = self.select_query_with_where_clause(tableName, tupleIdentifier, columnName)
    #         #self.logger.debug(query)
    #     try:
    #         self.execute_query(query)
    #         self.result = self.get_cursor().fetchall()
    #         #self.logger.debug(self.result)
    #     except sqlite3.DatabaseError as e:
    #         #self.logger.error("Error in executing SELECT query!")
    #         raise e
    #     
    # def select_query_with_where_clause(self, tableName, tupleIdentifier, columnName):
    #     """ Returns query with WHERE clause
    #     """
    #     if columnName == '*':
    #             queryString = 'SELECT * FROM '+tableName+' WHERE '+tupleIdentifier[0]+'=\''+tupleIdentifier[1]+'\''
    #     else:
    #         queryString = "SELECT "+columnName+" FROM "+tableName+" WHERE "+tupleIdentifier[0]+"='"+tupleIdentifier[1]+"'"
    #     return queryString
    # 
    # def select_query_without_where_clause(self, tableName, tupleIdentifier, columnName):
    #     """ Returns query without WHERE clause
    #     """
    #     if columnName == '*':
    #             queryString = 'SELECT * FROM '+tableName
    #     else:
    #         queryString = 'SELECT '+columnName+' FROM '+tableName
    #     return queryString
    #===========================================================================
        
    def update_query(self, query):
        """ Updates specified table
        """
        try:
            self.logger.debug('Begin')
            self.execute_query("PRAGMA foreign_keys = OFF")
            self.execute_query(query)
            self.execute_query("PRAGMA foreign_keys = ON")
            self.logger.info("Update Completed.")
            self.logger.debug('End')
        except sqlite3.DatabaseError as e:
            self.logger.error("Error in executing UPDATE query!")
            raise e
            
    def delete_query(self, query):
        """ Deletes data from given table
        """
        try:
            self.logger.debug('Begin')
            self.execute_query(query)
            self.db_connection.commit()
            self.logger.debug('End')
        except sqlite3.DatabaseError as e:
            self.logger.error("Error in executing query!")
        
    def close_connection(self):
        """ Close database connection
        """
        try:
            self.db_connection.close()
            self.logger.info("Connection Closed.")
        except sqlite3.DatabaseError as e:
            self.logger.error("Error in Closing database connection!")
            raise e

   
        
if __name__ == "__main__":
    params = {"ip":"10.198.128.76", "username":"administrator", "password":"shoreadmin1"}
    obj_sqlite = SQLiteDBHandler(params)
    #obj_sqlite.connect_to_sqlite()
    #obj_sqlite.copb()
    obj_sqlite.create_connection('D:\Shoretel\RoD\system.db')
    obj_sqlite.select_query('users', ['first_name', 'tester1'])
    #obj_sqlite.insert_query("sites", 'site51', '11.198.1.5', 'admin1', 'changeme', 'hq1')
    ##obj_sqlite.close_connection()
    
    #obj_sqlite.update_query('sites', '2', name='ukumar', age=4)
        
        
