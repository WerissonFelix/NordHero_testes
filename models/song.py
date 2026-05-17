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
    file_path: str
    duration_seconds: int