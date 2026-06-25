from DataBase.repositories.base_repository import BaseRepository
from models.userXp import UserXp
from models.xpResult import XpResult
from models.story_progress import StoryProgress
class XpRepository(BaseRepository):
    def get_user_xp(self, user_id: int) -> dict:
        query = "SELECT * FROM user_xp WHERE user_id = ?" 
        row = self.fetchone(query, (user_id,))
        
        if row is None:
            query = "INSERT OR IGNORE INTO user_xp (user_id, total_xp, level) VALUES (?, 0, 1)"
            self.execute(query, (user_id,))
            
            xp_id, total_xp, level = None, 0, 1
        else:
            xp_id, userID, total_xp, level = row

        xp_in_level, xp_to_next = xp_progress_in_level(total_xp)
        return UserXp(id=xp_id, user_id=user_id, total_xp=total_xp, level=level, xp_in_level=xp_in_level, xp_to_next_level=xp_to_next,)

    def add_xp(self, user_id: int, rank: str, accuracy: float) -> XpResult:
        current = self.get_user_xp(user_id)
        old_level = current.level

        xp_earned = calculate_xp_earned(rank, accuracy)
        new_total = current.total_xp + xp_earned
        new_level = level_from_xp(new_total)

        query = """
            INSERT INTO user_xp (user_id, total_xp, level)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET total_xp = ?, level = ?
            """
        self.execute(query, (user_id, new_total, new_level, new_total, new_level))

        return XpResult(xp_earned = xp_earned, leveled_up = new_level > old_level, xp_data = self.get_user_xp(user_id))
    
    def get_completed_phase_numbers(self, user_id: int, difficulty_id: int) -> set[int]:
        return {phase.phase_number for phase in self.get_completed_phases(user_id, difficulty_id)}
    
    def get_completed_phases(self, user_id: int, difficulty_id: int) -> set[StoryProgress]:
        query = """
        SELECT * FROM story_progress
        where user_id = ? and difficulty_id = ?
        """
        rows = self.fetchall(query, (user_id, difficulty_id))
        return [StoryProgress(*row) for row in rows]

    def complete_phase(self, user_id: int, difficulty_id: int, song_id: int, phase_number: int) -> bool:
        try:
            self.execute(
                """
                INSERT INTO story_progress (user_id, difficulty_id, song_id, phase_number)
                VALUES (?, ?, ?, ?)
                """,
                (user_id, difficulty_id, song_id, phase_number)
            )
            return True
        except Exception:
            return False

    def is_phase_unlocked(self, user_id: int, difficulty_id: int, phase_number: int) -> bool:
        if phase_number <= 1:
            return True
        completed_numbers = self.get_completed_phase_numbers(user_id, difficulty_id)
        return (phase_number - 1) in completed_numbers 

    def get_max_unlocked_phase(self, user_id: int, difficulty_id: int) -> int:
        completed_numbers = self.get_completed_phase_numbers(user_id, difficulty_id)
        if not completed_numbers:
            return 1
        return max(completed_numbers) + 1
XP_BY_RANK = {
    "S":   500,
    "A":   300,
    "B":   150,
    "D":    50,
    "N/A":  10,
}

XP_PER_LEVEL = 1000

def xp_for_level(level: int) -> int:
    return (level - 1) * XP_PER_LEVEL

def level_from_xp(total_xp: int) -> int:
    return (total_xp // XP_PER_LEVEL) + 1

def xp_progress_in_level(total_xp: int) -> tuple[int, int]:
    return (total_xp % XP_PER_LEVEL, XP_PER_LEVEL)

def calculate_xp_earned(rank: str, accuracy: float) -> int:
    base = XP_BY_RANK.get(rank, 10)
    bonus = int(round(accuracy))
    return base + bonus