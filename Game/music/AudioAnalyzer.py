import librosa
import numpy as np


class AudioAnalyzer:
    def __init__(self,music_path):
        self.music_path = music_path
        self.notes = []
        self.time =  120 # Fallback
    
    def Generate_map(self):
        signal_wave, sample_rate = librosa.load(self.music_path + ".mp3")
         # librosa.load retorna: um numpy array e um int, sendo, respectivamente, o nome das variáveis

        time, beat_frames = librosa.beat.beat_track(y=signal_wave, sr=sample_rate)
        beat_times = librosa.frames_to_time(beat_frames, sr=sample_rate)
        time = float(np.squeeze(time))

        print(f"Tempo detectado: {time} BPM")
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

                self.notes.append([beat_time, lane])

        return self.notes, self.time
