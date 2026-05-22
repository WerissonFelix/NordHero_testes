from DataBase.dbpath import db_path
import sqlite3 

class BaseRepository:
    
    def __init__(self, db_path=db_path):
        self.db_path = db_path
    
    def connect(self):
        return sqlite3.connect(self.db_path)
    
    def execute(self, query, params = ()):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
    
    def fetchone(self, query, params = ()):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
    
    def fetchmany(self, query, params = ()):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchmany()
     
    def fetchall(self, query, params = ()):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()