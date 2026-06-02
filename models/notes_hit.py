from dataclasses import dataclass


@dataclass
class NotesHit:
    id: int | None
    chart_id: int
    
    qtd_miss: int
    qtd_bad: int
    qtd_good: int
    qtd_perfect: int
