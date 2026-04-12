from DataBase.tables import connection,cursor


def select_user(email: str = None, user_id: int = None):
    if email is not None:
        cursor.execute("select * from user where email = ?", (email,))

    elif user_id is not None:
        cursor.execute("select * from user where id = ?", (user_id,))

    user = cursor.fetchone()
    return user