from dataclasses import dataclass

@dataclass
class User:
    """
    Representa um usuário do sistema
    """
    
    id: int | None
    
    name: str | None
    telefone: str | None
    email: str
    password: str
    
    