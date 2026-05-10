from dataclasses import dataclass

@dataclass
class User:
    """
    Representa um usuário do sistema
    """
    
    id: int
    
    name: str
    email: str
    password: str
    
    