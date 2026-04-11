
from password_validator import PasswordValidator


class PasswordValidate:
    def __init__(self,password: str):
        self.password = password
        self.schema = PasswordValidator()
        self.validation_results = {}
        self.error_messages = {
            "len_valid": "A senha deve ter 8 a 20 caracteres",
            "has_num": "A senha deve ter pelo menos 1 número",
            "has_symbols": "A senha deve ter pelo menos 1 símbolo",
            "has_spaces": "A senha não pode conter espaços"
        }
    def validate(self):
        self.verify_exceptions()
        print(self.validation_results)
        if False not in self.validation_results.values() :
            return self.password, True
        else:
            errors = self.get_error_messages()
            return errors, False


    def verify_exceptions(self):
        len_valid = self.schema.min(8).max(20).validate(self.password)

        has_num = self.schema.has().digits().validate(self.password)

        has_symbols = self.schema.has().symbols().validate(self.password)

        has_spaces = self.schema.has().spaces().validate(self.password)

        self.validation_results = {
            "len_valid": len_valid,
            "has_num": has_num,
            "has_symbols": has_symbols,
            "has_spaces": not has_spaces
        }

    def get_error_messages(self) -> list:
        return [
            self.error_messages[k]
            for k,v in self.validation_results.items()
            if v == False
        ]


