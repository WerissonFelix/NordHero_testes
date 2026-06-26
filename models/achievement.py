from dataclasses import dataclass

@dataclass
class Achievement:
    id: int | None
    key: str
    name: str
    description: str
    icon: str

@dataclass
class UserAchievement:
    id: int | None
    user_id: int
    achievement_id: int
    unlocked_at: str