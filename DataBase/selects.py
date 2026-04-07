from DataBase.tables import connection,cursor


def select_user(email):

    cursor.execute("select * from user where email = ?", (email,))
    user = cursor.fetchone()
    return user