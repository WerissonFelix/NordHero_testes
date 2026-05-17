from pathlib import Path
from models.song import Song
from pygame import mixer

cwd = Path.cwd()

game_path = Path("Game")

music_path = Path("music")

file_path = cwd / game_path / music_path

list_musics = []
mixer.init()
for entry in file_path.iterdir():
    if entry.suffix == ".mp3":
        music = mixer.Sound(str(entry))
        list_musics.append(Song(
            None,
            entry.stem,
            " ",
            0.0,
            int(music.get_length())
        ))
        
print(list_musics)

print(file_path)