from dataclasses import dataclass
from models.userXp import UserXp

@dataclass
class XpResult:
    xp_earned: int
    leveled_up: bool
    xp_data: UserXp