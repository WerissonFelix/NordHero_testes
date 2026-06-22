from DataBase.repositories.base_repository import BaseRepository
from models.achievement import Achievement, UserAchievement

class AchievementRepository(BaseRepository):

    def get_all(self) -> list[Achievement]:
        rows = self.fetchall("SELECT id, key, name, description, icon FROM achievements")
        return [Achievement(*row) for row in rows] if len(rows) > 0 else None

    def get_by_key(self, key: str) -> Achievement | None:
        query = "SELECT id, key, name, description, icon FROM achievements WHERE key = ?"
        row = self.fetchone(query,(key,))
        
        if row is None:
            return None
        
        return Achievement(*row)

    def get_unlocked_by_user(self, user_id: int) -> list[UserAchievement]:
        query = "SELECT id, user_id, achievement_id, unlocked_at FROM user_achievements WHERE user_id = ?"
        
        rows = self.fetchall(query, (user_id,))
        
        return [UserAchievement(*row) for row in rows]

    def get_unlocked_keys_by_user(self, user_id: int) -> set[str]:
        query = """
            SELECT achievements.key
            FROM user_achievements
            INNER JOIN achievements ON achievements.id = user_achievements.achievement_id
            WHERE user_achievements.user_id = ?
            """
            
        rows = self.fetchall(query, (user_id,))
        
        return {row[0] for row in rows}

    def unlock(self, user_id: int, achievement_key: str) -> bool:
        achievement = self.get_by_key(achievement_key)
        if achievement is None:
            return False
        try:
            self.execute(
                "INSERT INTO user_achievements (user_id, achievement_id) VALUES (?, ?)",
                (user_id, achievement.id)
            )
            return True
        except Exception:
            return False

    def count_scores_by_user(self, user_id: int) -> int:
        row = self.fetchone("SELECT COUNT(*) FROM scores WHERE user_id = ?", (user_id,))
        return row[0] if row else 0

    def count_s_ranks_by_user(self, user_id: int) -> int:
        row = self.fetchone(
            "SELECT COUNT(DISTINCT chart_id) FROM scores WHERE user_id = ? AND rank = 'S'",
            (user_id,)
        )
        return row[0] if row else 0

    def has_rank_at_least(self, user_id: int, min_rank: str) -> bool:
        rank_order = {"S": 4, "A": 3, "B": 2, "D": 1}
        min_val = rank_order.get(min_rank, 0)
        rows = self.fetchall("SELECT DISTINCT rank FROM scores WHERE user_id = ?", (user_id,))
        return any(rank_order.get(row[0], 0) >= min_val for row in rows)

    def has_perfect_game(self, user_id: int) -> bool:
        row = self.fetchone(
            "SELECT COUNT(*) FROM notes_hit WHERE user_id = ? AND qtd_miss = 0",
            (user_id,)
        )
        return (row[0] if row else 0) > 0

    def total_perfects_by_user(self, user_id: int) -> int:
        row = self.fetchone(
            "SELECT COALESCE(SUM(qtd_perfect), 0) FROM notes_hit WHERE user_id = ?",
            (user_id,)
        )
        return row[0] if row else 0

    def total_good_plus_perfect_by_user(self, user_id: int) -> int:
        row = self.fetchone(
            "SELECT COALESCE(SUM(qtd_good + qtd_perfect), 0) FROM notes_hit WHERE user_id = ?",
            (user_id,)
        )
        return row[0] if row else 0

    def has_played_on_hard(self, user_id: int) -> bool:
        row = self.fetchone(
            """
            SELECT COUNT(*) FROM scores
            INNER JOIN song_charts ON song_charts.id = scores.chart_id
            WHERE scores.user_id = ? AND song_charts.difficulty_id = 3
            """,
            (user_id,)
        )
        return (row[0] if row else 0) > 0

    def has_good_rank_on_hard(self, user_id: int) -> bool:
        rank_ok = ("S", "A", "B")
        rows = self.fetchall(
            """
            SELECT scores.rank FROM scores
            INNER JOIN song_charts ON song_charts.id = scores.chart_id
            WHERE scores.user_id = ? AND song_charts.difficulty_id = 3
            """,
            (user_id,)
        )
        return any(row[0] in rank_ok for row in rows)

    def count_distinct_songs_played(self, user_id: int) -> int:
        row = self.fetchone(
            """
            SELECT COUNT(DISTINCT song_charts.song_id) FROM scores
            INNER JOIN song_charts ON song_charts.id = scores.chart_id
            WHERE scores.user_id = ?
            """,
            (user_id,)
        )
        return row[0] if row else 0

    def total_songs_in_game(self) -> int:
        row = self.fetchone("SELECT COUNT(*) FROM songs")
        return row[0] if row else 0

    def has_played_2players(self, user_id: int) -> bool:
        row = self.fetchone(
            """
            SELECT COUNT(*) FROM scores
            INNER JOIN song_charts ON song_charts.id = scores.chart_id
            INNER JOIN multiplayer_songs ON multiplayer_songs.instrumental_song = song_charts.song_id
                OR multiplayer_songs.vocal_song = song_charts.song_id
            WHERE scores.user_id = ?
            """,
            (user_id,)
        )
        return (row[0] if row else 0) > 0