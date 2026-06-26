from dataclasses import dataclass

@dataclass
class StoryProgress:
    id: int | None
    user_id: int
    difficulty_id: int
    song_id: int
    phase_number: int
    type_story: str
    completed_at: str