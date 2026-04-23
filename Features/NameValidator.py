import re

class NameValidator:
    def __init__(self, name: str):
        self.name = name.strip()
        self.message_error = None
    def validate(self):
        if len(self.name) < 3:
            self.message_error = "Nome muito curto"
            return self.message_error, False
       
        if len(self.name) > 35:
            self.message_error = "Nome muito"
            return "Nome muito longo", False

        if not re.match(r"^[A-Za-zÀ-ÿ\s]+$", self.name):
            return "Nome deve conter apenas letras", False

        return self.name, True
    
nome = "Werisson felix dos Santos Freitas"

print(len(nome.strip()))