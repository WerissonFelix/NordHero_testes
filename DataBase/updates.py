import sqlite3
from DataBase.tables import connection, cursor

def update_user(id_user, nome: str = None, email: str = None):
    """
    Atualiza dados de um usuário no banco de dados.
    
    Permite atualizar nome e/ou email de um usuário específico.
    Cada campo é atualizado independentemente.
    Após atualização, busca e retorna os dados completos do usuário.
    
    """

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


