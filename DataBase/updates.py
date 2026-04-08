import sqlite3
from DataBase.tables import connection, cursor

def update_user(id_user, nome, email, senha):
    print(id_user, nome, email, senha)
    query = "UPDATE user SET name = ?, email = ? WHERE id = ?"
    cursor.execute(query, (nome, email, id_user))
    connection.commit()

    cursor.execute("SELECT * FROM user WHERE id = ?", (id_user,))
    user = cursor.fetchone()
    return user


