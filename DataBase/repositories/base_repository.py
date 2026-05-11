import sqlite3 
import os

project_path = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(project_path, "Banco.db")
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
        
repository = BaseRepository()

# criar tabela
repository.execute("""
CREATE TABLE IF NOT EXISTS test (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
""")

# inserir dado
repository.execute("""
INSERT INTO test (name)
VALUES (?)
""", ("Werisson",))

# buscar um dado
result = repository.fetchone("""
SELECT * FROM test
WHERE name = ?
""", ("Werisson",))

print(result)

# buscar todos
results = repository.fetchall("""
SELECT * FROM test
""")

print(results)