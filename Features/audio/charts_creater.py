from DataBase.repositories.song_chart_repository import SongChartsRepository
from DataBase.repositories.song_repository import SongRepository
from DataBase.repositories.difficulty_repository import DifficultyRepository
from models.song_chart import SongChart
from models.difficulty import Difficulty


def create_all_charts():
    chartManeger = SongChartsRepository()
    songManeger = SongRepository()
    
    songs = songManeger.get_all()
    
    for song in songs: 
        all_charts = chartManeger.get_all_charts_by_song(song.id)
        
        for i in range(1,4):
            if all_charts is None:
                chart = SongChart(None, song.id, i, 0, 0)
                chartManeger.create(chart)
                continue
            else:
                break         

def create_one_chart(difficulty_id, song_id):
    chartManeger = SongChartsRepository()
 
    chart = SongChart(None, song_id, difficulty_id, 0, 0)
    chartManeger.create(chart)

create_all_charts()