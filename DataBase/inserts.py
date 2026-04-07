import sqlite3
from DataBase.tables import connection, cursor


def insert_user(name,email,password):
    cursor.execute("insert into user (name,email,password) values(?, ?, ?)",
                   (name,email,password))

    connection.commit()

    cursor.execute("select * from user where email = ?",(email,))
    user = cursor.fetchone()
    return user

