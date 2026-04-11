# Imports from App's Screens

from Screens.Home import home_screen
from Screens.Data_error import data_error_screen
from Screens.profile_options import profile_options_menu

# Data Base imports
from DataBase.inserts import insert_user
from DataBase.selects import select_user
from DataBase.updates import update_user

# Outhers Features imports
from Features.EmailValidator import EmailValidator
from Features.PasswordValidate import PasswordValidate


class DataVerifier:
    """
    Classe para verificar o resultado final de email e senha, e então,efetuar operaçõe no banco de dados.
    """
    def __init__(self, screen_name: str):
        self.screen_name = screen_name
        self.email_verified = None
        self.password_verified = None

    def verify_data(self, email, password, name: None, user_id: int = None):
        self.email_verified = EmailValidator(email.get_value())

        if self.screen_name == "creat_account":
            email_result, email_valid = self.email_verified.validate_for_create_screen()
        elif self.screen_name == "logon":
            email_result, email_valid = self.email_verified.validate_for_login_screen()
        else:
            email_result, email_valid = self.email_verified.validate_for_update_screen()

        if email_valid == False:
            print(email_result, email_valid)
            return data_error_screen(email_result, self.screen_name)

        self.password_verified = PasswordValidate(password.get_value())
        password_result, password_valid = self.password_verified.validate()

        if password_valid == False:
            print(password_result, password_valid)
            return data_error_screen(password_result, self.screen_name)

        return self.call_database_for_process(email,password, name,user_id)

    def call_database_for_process(self, email, password , name: None, user_id: int = None):
        if self.screen_name == "creat_account":
            user = insert_user(name.get_value(),email.get_value(),password.get_value())

        elif self.screen_name == "logon":
            user = select_user(email.get_value())

            if (user[2] == email.get_value() and user[3] == password.get_value()) == False:
                return data_error_screen("incorrect email or password", self.screen_name)
        else:
            user = update_user(user_id, name, email)

        return home_screen(user, profile_options_menu)
