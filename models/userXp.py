from dataclasses import dataclass

@dataclass
class UserXp:
    id: int | None
    user_id: int
    total_xp: int
    level: int
    xp_in_level: int
    xp_to_next_level: int