import sqlite3
from DataBase.tables import connection, cursor

def update_user(id_user, nome, email):
    query = "UPDATE user SET name = ?, email = ? WHERE id = ?"
    cursor.execute(query, (nome, email, id_user))
    connection.commit()

    cursor.execute("SELECT * FROM user WHERE id = ?", (id_user,))
    user = cursor.fetchone()
    return user


