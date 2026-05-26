from dataclasses import dataclass

@dataclass
class MultiplayerSong:
    """
    Representa uma música multiplayer do jogo para o modo multiplayer
    """
    
    id: int | None
    
    title: str
    instrumental_song: int
    vocal_song: int
    
    bpm: float 
    duration_seconds: int
    file_path: str
    story_difficulty_id: int