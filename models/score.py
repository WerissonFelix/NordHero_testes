from dataclasses import dataclass


@dataclass
class Score:
    """
    Representa uma partida jogada pelo usuário
    """
    id: int | None
    user_id: int
    chart_id: int
    
    score: int
    accuracy: float
    rank: str