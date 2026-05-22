from pathlib import Path
from models.song import Song
from DataBase.repositories.song_repository import SongRepository
from pygame import mixer

cwd = Path.cwd()

game_path = Path("Game")

music_path = Path("music")

file_path = cwd / game_path / music_path

list_musics = []

story_difficulty_map = {


    "Cafuné - tek it (instrumental)": 1,
    "Debussy - Clair de Lune - Rousseau (youtube)": 1,
    "Die With A Smile (Instrumental) - Lady Gaga": 1,
    "Imagine Dragons   Believer Official Instrumental - Anything And Everything (youtube)": 1,
    "Like Him (Instrumental) - Tyler the Creator - pb (abandoned) (youtube)": 1,
    "Ludovico Einaudi - Una Mattina (The Intouchables) - Rousseau (youtube)": 1,

    
    "I Thought I Saw Your Face Today - She & Him (Instrumental)": 2,
    "Fallen Down (Reprise) - Toby Fox (youtube)": 2,
    "Another One Bites The Dust - Instrumental": 2,
    "Michael Jackson  Billie Jean [Instrumental Version] - HIStoryWorldTourMJ (youtube)": 2,

    "Abolish the IRS": 3,
    "Ana Vidovic - Asturias by Isaac Albéniz -": 3,
    "MEGALOVANIA - Toby Fox": 3,  
  
}

mixer.init()
def load_and_register_music():
    for entry in file_path.iterdir():
        if entry.suffix == ".mp3":
            
            story_difficulty_id = story_difficulty_map[entry.stem]               
            music = mixer.Sound(str(entry))
            list_musics.append(Song(
                None,
                entry.stem,
                " ",
                0.0,
                int(music.get_length()),
                str(entry),
                story_difficulty_id 
       
            ))
    songManager = SongRepository()
    for music in list_musics:
        song_exists = songManager.get_by_title(music.title)
        
        if song_exists is not None:
            continue
        else:
            songManager.create(music)