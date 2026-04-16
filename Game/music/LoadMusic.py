from pygame import mixer


def play_song(song_name):
    mixer.init()
    mixer.music.load(song_name + ".mp3")
    mixer.music.play()