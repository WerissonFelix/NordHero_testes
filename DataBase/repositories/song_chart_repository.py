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
        select from song_charts
        where id = ?
        """
        row = self.fetchone(query, (chart_id,))
        
        if row is None:
            return
        
        return SongChart(row[0], row[1], row[2], row[3])
    
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
        