
from DataBase.repositories.base_repository import BaseRepository
from models.story_progress import StoryProgress

class StoryRepository(BaseRepository):
    def get_completed_phase_numbers(self, user_id: int, difficulty_id: int, type_story: str) -> set[int]:
        return {phase.phase_number for phase in self.get_completed_phases(user_id, difficulty_id, type_story)}
    
    def get_completed_phases(self, user_id: int, difficulty_id: int, type_story: str) -> set[StoryProgress]:
        query = """
        SELECT * FROM story_progress
        where (user_id = ? and difficulty_id = ? and type_story = ?)
        """
        rows = self.fetchall(query, (user_id, difficulty_id, type_story))
        return [StoryProgress(*row) for row in rows]

    def complete_phase(self, user_id: int, difficulty_id: int, song_id: int, phase_number: int, type_story: str) -> bool:
        try:
            self.execute(
                """
                INSERT INTO story_progress (user_id, difficulty_id, song_id, phase_number, type_story)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, difficulty_id, song_id, phase_number, type_story)
            )
            return True
        except Exception:
            return False

    def is_phase_unlocked(self, user_id: int, difficulty_id: int, phase_number: int, type_story) -> bool:
        if phase_number <= 1:
            return True
        completed_numbers = self.get_completed_phase_numbers(user_id, difficulty_id, type_story)
        return (phase_number - 1) in completed_numbers 

    def get_max_unlocked_phase(self, user_id: int, difficulty_id: int, type_story) -> int:
        completed_numbers = self.get_completed_phase_numbers(user_id, difficulty_id, type_story)
        if not completed_numbers:
            return 1
        return max(completed_numbers) + 1