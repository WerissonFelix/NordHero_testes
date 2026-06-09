import phonenumbers

class telefoneValidator:
    def __init__(self, telefone: str):
        self.telefone = telefone
        self.message_error = None

    def validar_telefone(self):
        try:
            parsed_number = phonenumbers.parse(self.telefone, None)
            
            is_valid = phonenumbers.is_valid_number(parsed_number)
            is_possible = phonenumbers.is_possible_number(parsed_number)

            return self.telefone, is_valid 

        except phonenumbers.NumberParseException:
            self.message_error = "Número inválido"
            return self.message_error, False
