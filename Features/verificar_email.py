from email_validator import validate_email, EmailNotValidError
from DataBase.selects import select_user

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
      else:
          emailinfo = validate_email(email, check_deliverability=True)
          email_verified = emailinfo.normalized

          return emailinfo.normalized, True
    except EmailNotValidError as e:
      error = str(e)

      return error, False
