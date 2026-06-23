from DataBase.repositories.base_repository import BaseRepository
from DataBase.tables import level_from_xp, xp_progress_in_level, calculate_xp_earned

class XpRepository(BaseRepository):
    def get_user_xp(self, user_id: int) -> dict:
        row = self.fetchone(
            "SELECT total_xp, level FROM user_xp WHERE user_id = ?",
            (user_id,)
        )
        if row is None:
            self.execute(
                "INSERT OR IGNORE INTO user_xp (user_id, total_xp, level) VALUES (?, 0, 1)",
                (user_id,)
            )
            total_xp, level = 0, 1
        else:
            total_xp, level = row

        xp_in_level, xp_to_next = xp_progress_in_level(total_xp)
        return {
            "total_xp": total_xp,
            "level": level,
            "xp_in_level": xp_in_level,
            "xp_to_next_level": xp_to_next,
        }

    def add_xp(self, user_id: int, rank: str, accuracy: float) -> dict:
        current = self.get_user_xp(user_id)
        old_level = current["level"]

        xp_earned = calculate_xp_earned(rank, accuracy)
        new_total = current["total_xp"] + xp_earned
        new_level = level_from_xp(new_total)

        self.execute(
            """
            INSERT INTO user_xp (user_id, total_xp, level)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET total_xp = ?, level = ?
            """,
            (user_id, new_total, new_level, new_total, new_level)
        )

        xp_in_level, xp_to_next = xp_progress_in_level(new_total)
        return {
            "xp_earned": xp_earned,
            "total_xp": new_total,
            "level": new_level,
            "leveled_up": new_level > old_level,
            "xp_in_level": xp_in_level,
            "xp_to_next_level": xp_to_next,
        }


    def get_completed_phases(self, user_id: int, difficulty_id: int) -> set[int]:
        rows = self.fetchall(
            "SELECT phase_number FROM story_progress WHERE user_id = ? AND difficulty_id = ?",
            (user_id, difficulty_id)
        )
        return {row[0] for row in rows}

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
        completed = self.get_completed_phases(user_id, difficulty_id)
        return (phase_number - 1) in completed

    def get_max_unlocked_phase(self, user_id: int, difficulty_id: int) -> int:
        completed = self.get_completed_phases(user_id, difficulty_id)
        if not completed:
            return 1
        return max(completed) + 1