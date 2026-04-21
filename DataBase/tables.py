import sqlite3
import os

project_path = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(project_path, "Banco.db")

connection  = sqlite3.connect(db_path)

#Curso é tipo uma ponte que manda uma ação pro banco, tipo isso
cursor = connection.cursor()

def table_user():
    query = """
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name varchar(255) NOT NULL,
            email varchar(255) NOT NULL UNIQUE,
            password varchar(255) NOT NULL
        )
    """

    cursor.execute(query)
    connection.commit()

    print("Table user created successfully")

table_user()




