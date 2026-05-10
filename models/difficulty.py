from dataclasses import dataclass

@dataclass
class Difficulty:
    """
    Representa uma dificuldade do jogo
    """
    
    id: int | None
    
    name: str