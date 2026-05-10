from dataclasses import dataclass

@dataclass
class Song:
    """
    Representa uma música do jogo
    """
    
    id: int | None
    
    title: str
    artist: str
    
    bpm: float
    duration_seconds: int