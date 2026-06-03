from pathlib import Path

from DataBase.repositories.song_repository import SongRepository
from DataBase.repositories.multiplayer_songs_repository import MultiplayerSongsRepository

from models.multiplayer_song import MultiplayerSong
from models.song import Song

from Features.audio.charts_creater import create_all_charts
from pygame import mixer

cwd = Path.cwd()

game_path = Path("Game")

music_path = Path("music")

file_path = cwd / game_path / music_path


story_difficulty_map = {
    
    "Cafuné - tek it (instrumental)": (1, "Instrumental"),
    "Debussy - Clair de Lune - Rousseau (youtube)": (1, "Instrumental"),
    "Die With A Smile (Instrumental) - Lady Gaga": (1, "Instrumental"),
    "Imagine Dragons   Believer Official Instrumental - Anything And Everything (youtube)": (1, "Instrumental"),
    "Like Him (Instrumental) - Tyler the Creator - pb (abandoned) (youtube)": (1, "Instrumental"),
    "Ludovico Einaudi - Una Mattina (The Intouchables) - Rousseau (youtube)": (1, "Instrumental"),
    
    "I Thought I Saw Your Face Today - She & Him (Instrumental)": (2, "Instrumental"),
    "Fallen Down (Reprise) - Toby Fox (youtube)": (2, "Instrumental"),
    "Another One Bites The Dust - Instrumental": (2, "Instrumental"),
    
    "I Thought I Saw Your Face Today (Acapella_Vocals Only)": (2, "Vocal"),
    "Another One Bites The Dust - Queen  Vocal": (2, "Vocal"),
    "Imagine Dragons - BELIEVER Vocal": (1, "Vocal"),
    "Michael Jackson - Billie Jean Vocals Only": (2, "Vocal"),
    "Michael Jackson  Billie Jean [Instrumental Version] - HIStoryWorldTourMJ (youtube)": (2, "Instrumental"),

    "Abolish the IRS": (3, "Instrumental"),
    "Ana Vidovic - Asturias by Isaac Albéniz -": (3, "Instrumental"),
    "MEGALOVANIA - Toby Fox": (3, "Instrumental"),
    
    "Z I Thought I Saw Your Face Today (FULL)": (
        2, "Full",
        "I Thought I Saw Your Face Today - She & Him (Instrumental)", 
        "I Thought I Saw Your Face Today (Acapella_Vocals Only)"
    ),
}

mixer.init()
def load_and_register_music():
    songManager = SongRepository()
    multiplayerManager = MultiplayerSongsRepository()
    
    for entry in file_path.iterdir():
        if entry.suffix == ".mp3":
            
            music_info = story_difficulty_map[entry.stem]               
            
            story_difficulty_id = music_info[0]
            music_type = music_info[1]
            
            music = mixer.Sound(str(entry))
                
            if music_type == "Full":
                song_exists = multiplayerManager.get_by_title(entry.stem)
                if song_exists is None:
                    instrumental = songManager.get_by_title(music_info[2])
                    vocal = songManager.get_by_title(music_info[3])
                    
                    multiplayerManager.create(MultiplayerSong(
                        None,
                        entry.stem,
                        instrumental.id,
                        vocal.id,
                        0.0,
                        int(music.get_length()),
                        str(entry),
                        story_difficulty_id 
                    ))
                else:
                    continue
            else:
                song_exist = songManager.get_by_title(entry.stem)
                if song_exist is None:
                    songManager.create(Song(
                        None,
                        entry.stem,
                        music_type,
                        0.0,
                        int(music.get_length()),
                        str(entry),
                        story_difficulty_id     
                    ))
                else:
                    continue
    create_all_charts()

load_and_register_music()