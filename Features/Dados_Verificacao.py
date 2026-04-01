
# Imports from installed libraies
from email_validator import validate_email, EmailNotValidError
from password_validator import PasswordValidator
from password_validator.lib import uppercase

# Imports from App's Screens
from Screens.Home import home_screen
from Screens.Data_error import data_error_screen

def verificar_dados(nome,email,senha,screen_name):
    email_verificado, validade_email = verificar_email(email.get_value())
    senha_verificada, validade_senha = verifcar_senha(senha.get_value())

    if validade_senha and validade_email:
        dados = {"nome": nome.get_value(), "email": email_verificado, "senha" : senha_verificada}
        return home_screen(dados)
    elif validade_email == False:
        return data_error_screen(email_verificado, screen_name)
    else:
        return data_error_screen(senha_verificada, screen_name)

def verificar_email(email):
    try:
      # Check that the email address is valid. Turn on check_deliverability
      # for first-time validations like on account creation pages (but not
      # login pages).
      emailinfo = validate_email(email, check_deliverability=True)
      # After this point, use only the normalized form of the email address,
      # especially before going to a database query.
      email = emailinfo.normalized
      return email, True


    except EmailNotValidError as e:

      # The exception message is human-readable explanation of why it's
      # not a valid (or deliverable) email address.
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






