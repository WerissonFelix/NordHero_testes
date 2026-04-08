
from DataBase.inserts import connection,cursor

# Screens Import


def delete_user(id_user,email):
    from Screens.Inital import initial_screen
    from Screens.Logon import login_screen
    from Screens.Creat_Account import create_account_menu
    query = "delete from user where id = ?"

    cursor.execute(query,(id_user,))
    connection.commit()

    """
    try: 
        cursor.execute("select * from user where email = ?",(email,))
        connection.commit()
        
        user = cursor.fetchone()
            
    except:
    """

    return initial_screen(login_screen,create_account_menu)







