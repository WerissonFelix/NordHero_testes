import sqlite3
from DataBase.tables import connection, cursor

def update_user(id_user, nome: str = None, email: str = None):

    if nome is not None:
        query = "UPDATE user SET name = ? WHERE id = ?"
        cursor.execute(query, (nome, id_user))

    if email is not None:
        query = "UPDATE user SET email = ? WHERE id = ?"
        cursor.execute(query, (email, id_user))

    connection.commit()

    cursor.execute("SELECT * FROM user WHERE id = ?", (id_user,))
    user = cursor.fetchone()

    return user


