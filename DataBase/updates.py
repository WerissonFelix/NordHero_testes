import sqlite3
from DataBase.tables import connection, cursor

def update_user(id, nome, email, senha):
    print(id,nome,email,senha)
    query = "UPDATE user SET name = ?, email = ? WHERE id = ?"
    cursor.execute(query,(nome,email,id))
    connection.commit()

    cursor.execute("SELECT * FROM user WHERE id = ?", (id,))
    user = cursor.fetchone()
    return user


