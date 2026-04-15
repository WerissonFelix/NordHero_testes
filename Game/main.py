import pygame
from pygame import mixer

import librosa
import numpy as np

def generate_map(music_name):
    signal_wave, sample_rate = librosa.load(music_name + ".mp3")
    # librosa.load retorna: um numpy array e um int, sendo, respectivamente, o nome das variáveis

    tempo, beat_frames = librosa.beat.beat_track(y=signal_wave, sr=sample_rate)
    beat_times = librosa.frames_to_time(beat_frames, sr=sample_rate)
    tempo = float(np.squeeze(tempo))

    print(f"Tempo detectado: {tempo} BPM")
    print(f"Total de beats: {len(beat_times)}")

    S = np.abs(librosa.stft(y=signal_wave))
    freqs = librosa.fft_frequencies(sr=sample_rate)

    all_freqs = []

    # Analisa APENAS nos beats detectados
    for beat_time in beat_times:
        # Converte tempo para frame
        frame = int(librosa.time_to_frames(beat_time, sr=sample_rate))

        if frame < S.shape[1]:

            spectrum = S[:, frame]
            freq = freqs[np.argmax(spectrum)]

            all_freqs.append(freq)

    if all_freqs:
        percentiles = np.percentile(all_freqs, [25, 50, 75])
    else:
        percentiles = [150,600,2000]
    notes = []

    for beat_time in beat_times:
        frame = int(librosa.time_to_frames(beat_time, sr=sample_rate))

        if frame < S.shape[1]:
            spectrum = S[:, frame]
            freq = freqs[np.argmax(spectrum)]

            if freq < percentiles[0]:
                lane = 0
            elif freq < percentiles[1]:
                lane = 1
            elif freq < percentiles[2]:
                lane = 2
            else:
                lane = 3

            notes.append([beat_time, lane])

    return notes, tempo

pygame.init()
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
mixer.init()


class Key:
    def __init__(self, x, y, color1, color2, key):
        self.x = x
        self.y = y
        self.color1 = color1
        self.color2 = color2
        self.key = key
        self.rect = pygame.Rect(self.x,self.y,100,40)
        self.active = True

keys = [
    Key(200,500,(255,0,0), (220,0,0),pygame.K_a),
    Key(300,500,(0,255,0), (0,220,0),pygame.K_s),
    Key(400,500,(0,0,255), (0,0,220),pygame.K_d),
    Key(500,500,(255,255,0), (220,220,0),pygame.K_f),
]


#I Thought I Saw Your Face Today
music2 = "I Thought I Saw Your Face Today"
music = "I Thought I Saw Your Face Today - She & Him (Instrumental)"

notess, tempo = generate_map(music)

print(f"Música analisada com {tempo} BPM")
print(f"Total de notas geradas: {len(notess)}")


mixer.music.load("I Thought I Saw Your Face Today - She & Him (Instrumental).mp3")
mixer.music.play()

spawn_offset = 1.5

base_speed = 300
speed = base_speed * (tempo / 120)

score = 0
font = pygame.font.Font("freesansbold.ttf", 30)

while True:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    screen.fill((0,0,0))
    keys_pressed = pygame.key.get_pressed()
    current_time = mixer.music.get_pos() / 1000
    for key in keys:
        # Verifica se a tecla está pressionada

        if keys_pressed[key.key]:
            pygame.draw.rect(screen, key.color2, key.rect)
            key.handled = True
        else:
            pygame.draw.rect(screen, key.color1, key.rect)
            key.handled = False

    notes_to_remove = []

    for note in notess:
        note_time, lane = note

        if note_time - spawn_offset <= current_time:
            time_diff = note_time - current_time
            y = 500 - (time_diff * speed)
            x = 200 + lane * 100

            rect = pygame.Rect(x, y, 50, 25)

            pygame.draw.rect(screen, (200,0,0),rect)

            if rect.colliderect(keys[lane].rect):
                if keys_pressed[keys[lane].key]:
                    notes_to_remove.append(note)
                    score += 100
            elif y > 600:
                notes_to_remove.append(note)

    for n in notes_to_remove:
        if n in notess:
            notess.remove(n)


    score_text = font.render(f"Score: {score}", True, (255,255,255))
    screen.blit(score_text, (10, 10))
    pygame.display.update()
    clock.tick(60)