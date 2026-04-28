
from DataBase.inserts import connection,cursor

# Screens Import


def delete_user(id_user,email):
    """
    Exclui um usuário do banco de dados e retorna à tela inicial.
    
    Remove permanentemente o registro do usuário baseado no ID
    e redireciona para a tela inicial do sistema.
    """
    
    from Screens.Inital import initial_screen
    from Screens.Logon import login_screen
    from Screens.Creat_Account import create_account_menu
    query = "delete from user where id = ?"

    cursor.execute(query,(id_user,))
    connection.commit()

    return initial_screen(login_screen,create_account_menu)







