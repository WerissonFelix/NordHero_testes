from DataBase.repositories.base_repository import BaseRepository
from models.song_chart import SongChart

class SongChartsRepository(BaseRepository):
    
    def create(self, chart: SongChart):
        query = """
        insert into song_charts (song_id, difficulty_id, max_possible_score, notes_count)
        values (?, ?, ?, ?)
        """
        self.execute(query, (chart.song_id, chart.difficulty_id, chart.max_possible_score, chart.notes_count))
    
    def get_by_id(self, chart_id):
        query = """
        select * from song_charts
        where id = ?
        """
        row = self.fetchone(query, (chart_id,))
        
        if row is None:
            return
        
        return SongChart(row[0], row[1], row[2], row[3], row[4])
    
    def update(self, chart_id):
        query = """
        update song_charts
        set song_id = ?, difficulty_id = ?,
        max_possible_score = ?, notes_count = ?
        where id = ?
        """
        
        self.execute(query, (chart_id, ))
    
    def delete(self, chart_id):
        query = """
        delete from song_charts
        where id = ?
        """
        
        self.execute(query, (chart_id,))
    
    def get_by_song_and_difficulty(self, song_id, difficulty_id):
        query = """
        select * from song_charts
        where (song_id = ? and difficulty_id = ?)
        """  
        
        row = self.fetchone(query, (song_id, difficulty_id))
        
        if row is None:
            return None
        
        return SongChart(row[0], row[1], row[2], row[3], row[4])
        
    def get_all_charts_by_song(self, song_id):
        query = """
        select * from song_charts
        where song_id = ?
        """
        
        rows = self.fetchall(query, (song_id, ))
        
        if len(rows) == 0:
            return None
        
        all_charts = []
        for row in rows:
            all_charts.append(SongChart(row[0], row[1], row[2], row[3], row[4]))
        
        return all_charts
        
    def get_all_charts_by_difficulty(self, difficulty_id):
        query = """
        select * from song_charts 
        where difficulty_id = ?
        """
        rows = self.fetchall(query, (difficulty_id, ))
        
        if rows in None:
            return None
        
        all_charts = []
        
        for row in rows:
            all_charts.append(SongChart(row[0], row[1], row[2], row[3], row[4]))
            
        return all_charts
            