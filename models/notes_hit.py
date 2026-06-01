from dataclasses import dataclass


@dataclass
class NotesHit:
    id: int | None
    
    qtd_miss: int
    qtd_good: int
    qtd_perfect: int
