from dataclasses import dataclass

@dataclass
class SongChart:
    """
    Representa o chart/mapa jogável de uma música
    """
    
    id: int | None
    
    song_id = int
    difficulty_id = int
    
    max_possible_score = int
    notes_count = int
    