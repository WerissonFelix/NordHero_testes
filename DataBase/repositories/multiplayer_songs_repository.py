from DataBase.repositories.base_repository import BaseRepository
from models.multiplayer_song import MultiplayerSong

class MultiplayerSongsRepository(BaseRepository):
    
    def create(self, multiplayer_song: MultiplayerSong):
        query = """
        insert into multiplayer_songs (title, instrumental_song, vocal_song, bpm, duration_seconds, file_path, story_difficulty_id)
        values (?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(query, (
            multiplayer_song.title,
            multiplayer_song.instrumental_song,
            multiplayer_song.vocal_song,
            multiplayer_song.bpm,
            multiplayer_song.duration_seconds,
            multiplayer_song.file_path,
            multiplayer_song.story_difficulty_id
        ))
        
    def get_by_id(self, id):
        query = """
        select * from multiplayer_songs
        where id = ?
        """
        
        row = self.fetchone(query, (id,))
        
        if row is None:
            return
        
        return MultiplayerSong(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            row[6],
            row[7]
        )
    
    def get_by_title(self, title):
        query = """
        select * from multiplayer_songs
        where title = ?
        """
        
        row = self.fetchone(query, (title,))
        
        if row is None:
            return
        
        return MultiplayerSong(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            row[6],
            row[7]
        )
        
    def get_by_instrumental_and_vocal(self, instrumental_song_id, vocal_song_id):
        query = """
        select * from multiplayer_songs
        where instrumental_song = ? and vocal_song = ?
        """
        
        row = self.fetchone(query, (instrumental_song_id, vocal_song_id))
        
        if row is None:
            return
        
        return MultiplayerSong(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            row[6],
            row[7]
        )
        
    def get_by_difficulty(self, story_difficulty_id):
        query = """
        select * from multiplayer_songs
        where story_difficulty_id = ?
        """
        
        all_songs = self.fetchall(query, (story_difficulty_id,))
        
        rows = []
        
        if len(all_songs) == 0:
            return None
        
        for row in all_songs:
            rows.append(
                MultiplayerSong(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[6],
                    row[7]
                )
            )
        
        return rows
    
    def get_all(self):
        query = """
        select * from multiplayer_songs
        """
        
        all_songs = self.fetchall(query)
        
        rows = []
        
        if len(all_songs) == 0:
            return None
        
        for row in all_songs:
            rows.append(
                MultiplayerSong(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[6],
                    row[7]
                )
            )
        
        return rows