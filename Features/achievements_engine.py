from DataBase.repositories.achievement_repository import AchievementRepository


class AchievementsEngine:

    def __init__(self):
        self.repository = AchievementRepository()

    def check_all(self, user_id: int) -> list:
        already_unlocked = self.repository.get_unlocked_keys_by_user(user_id)
        newly_unlocked = []

        checks = [
            ("first_note",   self._check_first_note),
            ("5_songs",      self._check_5_songs),
            ("20_songs",     self._check_20_songs),
            ("50_songs",     self._check_50_songs),
            ("first_s",      self._check_first_s),
            ("first_a",      self._check_first_a),
            ("3_s_ranks",    self._check_3_s_ranks),
            ("perfect_game", self._check_perfect_game),
            ("100_perfects", self._check_100_perfects),
            ("500_perfects", self._check_500_perfects),
            ("100_notes",    self._check_100_notes),
            ("first_hard",   self._check_first_hard),
            ("beat_hard",    self._check_beat_hard),
            ("play_all",     self._check_play_all),
            ("2players",     self._check_2players),
        ]

        for key, check_fn in checks:
            if key in already_unlocked:
                continue
            if check_fn(user_id):
                if self.repository.unlock(user_id, key):
                    achievement = self.repository.get_by_key(key)
                    if achievement:
                        newly_unlocked.append(achievement)

        return newly_unlocked

    def _check_first_note(self, user_id):
        return self.repository.count_scores_by_user(user_id) >= 1
    
    def _check_5_songs(self, user_id):
        return self.repository.count_scores_by_user(user_id) >= 5
    
    def _check_20_songs(self, user_id): 
        return self.repository.count_scores_by_user(user_id) >= 20
    
    def _check_50_songs(self, user_id):
        return self.repository.count_scores_by_user(user_id) >= 50
    
    def _check_first_s(self, user_id):
        return self.repository.has_rank_at_least(user_id, "S")
    
    def _check_first_a(self, user_id):
        return self.repository.has_rank_at_least(user_id, "A")
    
    def _check_3_s_ranks(self, user_id):
        return self.repository.count_s_ranks_by_user(user_id) >= 3
    
    def _check_perfect_game(self, user_id):
        return self.repository.has_perfect_game(user_id)
    
    def _check_100_perfects(self, user_id):
        return self.repository.total_perfects_by_user(user_id) >= 100
    
    def _check_500_perfects(self, user_id):
        return self.repository.total_perfects_by_user(user_id) >= 500
    
    def _check_100_notes(self, user_id): 
        return self.repository.total_good_plus_perfect_by_user(user_id) >= 100
    
    def _check_first_hard(self, user_id): 
        return self.repository.has_played_on_hard(user_id)
    
    def _check_beat_hard(self, user_id): 
        return self.repository.has_good_rank_on_hard(user_id)
    
    def _check_2players(self, user_id):  
        return self.repository.has_played_2players(user_id)

    def _check_play_all(self, user_id):
        total = self.repository.total_songs_in_game()
        played = self.repository.count_distinct_songs_played(user_id)
        return total > 0 and played >= total