from email_validator import validate_email, EmailNotValidError
from DataBase.selects import select_user

class EmailValidator:
    """
    Classe para validar email, pode validar para create, login e update,
    conforme padrões do sistema.

    Valida email para a create, login e update screens, pode retornar uma mensagem de erro
    ou o email verificado, em ambos os casos, retornará uma tupla: (str, bool)

    """
    def __init__(self, email: str):
        self.email = email
        self.email_verified = None
        self.message_error = None
    def validate_for_create_screen(self) -> tuple:
        """
        Valida email para tela de criação de conta.
        """
        try:
            email_info = validate_email(self.email, check_deliverability=True)
            self.email_verified = email_info.normalized

            user_account = select_user(self.email)

            if user_account is None:
                return self.email_verified, True
            else:
                self.message_error = "email already registered"
                return self.message_error, False

        except EmailNotValidError as e:
            self.message_error = str(e)
            return self.message_error, False
    def validate_for_login_screen(self) -> tuple:
        """
        Valida email para tela de login.
        """
        
        try:
            email_info = validate_email(self.email, check_deliverability=False)
            self.email_verified = email_info.normalized

            user_account = select_user(self.email)

            if user_account is not None:
                return self.email_verified, True
            else:
                self.message_error = "email doesn't exist"
                return self.message_error, False

        except EmailNotValidError as e:
            self.message_error = str(e)
            return self.message_error, False
    def validate_for_update_screen(self) -> tuple:
        """
        Valida email para tela de atualização de perfil.
        """
        
        try:
            email_info = validate_email(self.email, check_deliverability=False)
            self.email_verified = email_info.normalized

            user_account = select_user(self.email)

            if user_account is None:
                return self.email_verified, True
            else:
                self.message_error = "email already registered"
                return self.message_error, False
        except EmailNotValidError as e:
            self.message_error = str(e)
            return self.message_error, False
