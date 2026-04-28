import re

class NameValidator:
    """
    Validador de nome de usuário para o sistema.

    Aplica regras de validação como tamanho mínimo/máximo e
    caracteres permitidos (apenas letras e espaços, incluindo acentos).
    """
        
    def __init__(self, name: str):
        self.name = name.strip()
        self.message_error = None
    def validate(self):
        """ 
        Valida o nome conforme regras do sistema
        """
        if len(self.name) < 3:
            self.message_error = "Nome muito curto"
            return self.message_error, False
       
        if len(self.name) > 20:
            self.message_error = "Nome muito"
            return "Nome muito longo", False

        if not re.match(r"^[A-Za-zÀ-ÿ\s]+$", self.name):
            return "Nome deve conter apenas letras", False

        return self.name, True