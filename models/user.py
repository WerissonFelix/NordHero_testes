from dataclasses import dataclass

@dataclass
class User:
    """
    Representa um usuário do sistema
    """
    
    id: int | None
    
    name: str | None
    email: str
    password: str
    
    