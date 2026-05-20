from DataBase.repositories.base_repository import BaseRepository
from models.song import Song


class SongRepository(BaseRepository):
    
    def create(self, song: Song):
        query = """
        insert into songs (title, artist, bpm, duration_seconds, file_path, story_difficulty_id)
        values (?, ?, ?, ?, ?, ?)
        """
        self.execute(query, (song.title, song.artist, song.bpm, song.duration_seconds, song.file_path, song.story_difficulty_id))
        
    def get_by_id(self, song_id):
        query = """
        select * from songs 
        where id = ?
        """
        row = self.fetchone(query, (song_id,))
        
        if row is None:
            return
        
        return Song(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        
    def get_by_title(self, song_id):
        query = """
        select * from songs
        where title = ?
        """
        
        row = self.fetchone(query, (song_id,))
        
        if row is None:
            return
        
        return Song(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
    
    def get_by_story_difficulty_id(self, story_difficulty_id):
        query = """
        select * from songs
        where story_difficulty_id = ?
        """
        
        all_songs = self.fetchall(query, (story_difficulty_id,))
        
        rows = []
        
        for row in all_songs:
            rows.append(
                Song(
                    row[0], 
                    row[1], 
                    row[2], 
                    row[3], 
                    row[4],
                    row[5],
                    row[6]
                )
            )
        
        return rows
    
    def get_by_file_path(self, file_path: str):
        query = """
        select * from songs
        where file_path = ?
        """
        
        row = self.fetchone(query, (file_path,))
        
        if row is None:
            return
        
        return Song(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
    
    def get_all(self):
        query = """
        select * from songs
        """
        
        all_songs = self.fetchall(query)
        
        rows = []
        
        for row in all_songs:
            rows.append(
                Song(
                    row[0], 
                    row[1], 
                    row[2], 
                    row[3], 
                    row[4],
                    row[5],
                    row[6]
                )
            )
        
        return rows
    
    def update_song_by_id(self, song: Song):
        query = """
        update songs
        set title = ?, artist = ?,
        bpm = ?, file_path = ?, duration_seconds = ?,
        story_difficulty_id = ? 
        where id = ?
        """
        
        self.execute(query, (song.title, song.artist, song.bpm, song.file_path, song.duration_seconds, song.story_difficulty_id, song.id))
        
    def delete_song(self, song_id):
        query = """
        delete from songs
        where id = ?
        """
        
        self.execute(query, (song_id,))   