from DataBase.repositories.base_repository import BaseRepository
from models.song import Song


class SongRepository(BaseRepository):
    
    def create(self, song: Song):
        query = """
        insert into songs (title, artist, bpm, duration_seconds)
        values (?, ?, ?, ?)
        """
        self.execute(query, (song.title, song.artist, song.bpm, song.duration_seconds))
        
    def get_by_id(self, song_id):
        query = """
        select * from songs 
        where id = ?
        """
        row = self.fetchone(query, (song_id,))
        
        if row is None:
            return
        
        return Song(row[0], row[1], row[2], row[3], row[4])
        
    def get_by_title(self, song_id):
        query = """
        select * from songs
        where title = ?
        """
        
        row = self.fetchone(query, (song_id,))
        
        if row is None:
            return
        
        return Song(row[0], row[1], row[2], row[3], row[4])
    
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
                    row[4]
                )
            )
        
        return rows
    
    def update_song_by_id(self, song: Song):
        query = """
        update songs
        set title = ?, artist = ?,
        bpm = ?, duration_seconds = ?
        where id = ?
        """
        
        self.execute(query, (song.title, song.artist, song.bpm, song.duration_seconds, song.id))
        
    def delete_song(self, song_id):
        query = """
        delete from songs
        where id = ?
        """
        
        self.execute(query, (song_id,))   