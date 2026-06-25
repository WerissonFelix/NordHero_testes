from dataclasses import dataclass
from models.song import Song

@dataclass
class Phase:
    number: int
    unlocked: bool
    song: Song
    done: bool