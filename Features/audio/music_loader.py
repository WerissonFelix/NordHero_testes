from pathlib import Path
from models.song import Song
from DataBase.repositories.song_repository import SongRepository
from pygame import mixer

cwd = Path.cwd()

game_path = Path("Game")

music_path = Path("music")

file_path = cwd / game_path / music_path

list_musics = []
mixer.init()
def load_and_register_music():
    for entry in file_path.iterdir():
        if entry.suffix == ".mp3":
            music = mixer.Sound(str(entry))
            list_musics.append(Song(
                None,
                entry.stem,
                " ",
                0.0,
                str(entry),
                int(music.get_length())
            ))
    songManager = SongRepository()
    for music in list_musics:
        song_exists = songManager.get_by_title(music.title)
        
        if song_exists is not None:
            continue
        else:
            songManager.create(music)