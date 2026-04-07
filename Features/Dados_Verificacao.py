
# Imports from installed libraies
from email_validator import validate_email, EmailNotValidError
from password_validator import PasswordValidator

# Imports from App's Screens
from Screens.Home import home_screen
from Screens.Data_error import data_error_screen

# Data Base imports
from DataBase.inserts import insert_user
from DataBase.selects import select_user

def verificar_dados(nome,email,senha,screen_name):
    email_verificado, validade_email = verificar_email(email.get_value(),screen_name)
    senha_verificada, validade_senha = verifcar_senha(senha.get_value())

    if validade_senha and validade_email:
        if screen_name == "creat_account":
            user = insert_user(nome.get_value(),email_verificado,senha_verificada)
        else:
            user = select_user(email_verificado)

            if not (user[2] == email_verificado and user[3] == senha_verificada):
                mensagem_error = "Email ou senha incorreto"
                return data_error_screen(mensagem_error, screen_name)

        return home_screen(user)
    elif validade_email == False:

        return data_error_screen(email_verificado, screen_name)
    else:
        return data_error_screen(senha_verificada, screen_name)

def verificar_email(email, screen_name):
    try:

      if screen_name == "creat_account":
        emailinfo = validate_email(email, check_deliverability=True)
        user_account = select_user(email)

        if user_account is None:

            email_verified = emailinfo.normalized

            return email_verified, True
        else:

            mensagem_error = "email already registered"

            return mensagem_error, False
      elif screen_name == "logon":
          emailinfo = validate_email(email, check_deliverability=False)
          user_account = select_user(email)

          if user_account is not None:
              email_verified = emailinfo.normalized

              return email_verified, True
          else:
              message_error = "email doesn't exist"

              return message_error, False
    except EmailNotValidError as e:

      error = str(e)
      return error, False

def verifcar_senha(senha):
   schema = PasswordValidator()

   len_valido = schema.min(8).max(20).validate(senha)
   has_num = schema.has().digits().validate(senha)
   has_symbols = schema.has().symbols().validate(senha)
   spaces = schema.has().spaces().validate(senha)


   verificacao = {
       "len_valido": len_valido,
       "has_num": has_num,
       "has_symbols": has_symbols,
       "has_spaces": not spaces
   }

   mensagens_error = {
       "len_valido": "A senha deve ter 8 a 20 caracteres",
       "has_num": "A senha deve ter pelo menos 1 número",
       "has_symbols": "A senha deve ter pelo menos 1 símbolo",
       "has_spaces": "not spaces"
   }

   if False not in verificacao.values():
       return senha, True
   else:
       dados_errados = {mensagens_error[k]:v for k,v in verificacao.items() if v == False}

       return dados_errados, False

