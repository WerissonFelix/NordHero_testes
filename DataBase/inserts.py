import sqlite3
from DataBase.tables import connection, cursor


def insert_user(name,email,password):
    """
    Insere um novo usuário no banco de dados e retorna seus dados.
    
    Cria um registro na tabela 'user' com nome, email e senha,
    depois busca e retorna o usuário recém-criado para uso no sistema.
    
    """
    cursor.execute("insert into user (name,email,password) values(?, ?, ?)",
                   (name,email,password))

    connection.commit()

    cursor.execute("select * from user where email = ?",(email,))
    user = cursor.fetchone()
    return user

