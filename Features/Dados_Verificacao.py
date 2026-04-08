# Imports from App's Screens
from Screens.Home import home_screen
from Screens.Data_error import data_error_screen
from Screens.profile_options import profile_options_menu

# Data Base imports
from DataBase.inserts import insert_user
from DataBase.selects import select_user
from DataBase.updates import update_user

# Outhers Features imports
from Features.verificar_email import verificar_email
from Features.verificar_senha import verifcar_senha

def verificar_dados(screen_name,email,senha,nome=None, id=None):
    email_verificado, validade_email = verificar_email(email.get_value(),screen_name)
    senha_verificada, validade_senha = verifcar_senha(senha.get_value())

    if validade_senha and validade_email:
        if screen_name == "creat_account":
            user = insert_user(nome.get_value(),email_verificado,senha_verificada)
        elif screen_name == "logon":
            user = select_user(email_verificado)

            if not (user[2] == email_verificado and user[3] == senha_verificada):
                mensagem_error = "Email ou senha incorreto"
                return data_error_screen(mensagem_error, screen_name)
        else:

            user = update_user(id, nome.get_value(), email_verificado, senha_verificada)
        return home_screen(user, profile_options_menu)
    elif validade_email == False:

        return data_error_screen(email_verificado, screen_name)
    else:
        return data_error_screen(senha_verificada, screen_name)
