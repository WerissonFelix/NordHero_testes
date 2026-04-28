import librosa
import numpy as np
from pygame import mixer

class AudioAnalyzer:
    """ 
    Classe que analisa a música escolhida pelo user, seus
    métodos são usados somente quando o jogo começar.
    
    
    Responsável por extrair informações musicais de um arquivo MP3,
    gerar um mapa de notas sincronizado com os beats e classificar
    cada nota em lanes baseado na frequência dominante.
    """


    def __init__(self,music_path):
        self.music_path = music_path
        self.notes = []
        self.qtd_notes = 0
        self.time =  120 # Fallback
    
    def Generate_map(self):
        
        """
        
        Método mais importante do projeto. Ele gera o mapeamento das notas da música.
        
        Processo:
        1. Carrega o áudio com librosa
        2. Detecta BPM e posições dos beats
        3. Analisa frequências dominantes de cada beat
        4. Classifica cada beat em uma lane (0-3) baseado em percentis
        5. Retorna lista de notas [beat_time, lane] e BPM
        """
        signal_wave, sample_rate = librosa.load(self.music_path + ".mp3")
        # librosa.load retorna: um numpy array e um int, sendo, respectivamente, o nome das variáveis

        time, beat_frames = librosa.beat.beat_track(y=signal_wave, sr=sample_rate)
        beat_times = librosa.frames_to_time(beat_frames, sr=sample_rate)
        time = float(np.squeeze(time))

        # Esse frames_to_time é para obtermos o tempo real de cada beat que o beat_track achou
        # o squeeze é usado para garantir que time seja um float
        
        self.qtd_notes = len(beat_times)
        print(f"Tempo detectado: {time} BPM")
        print(f"Total de beats: {self.qtd_notes}")

        
        """

        A partir daqui ocorre a análise da frequência da música, aqui 
        o áudio é transformado em espectro, que é tipo uma mistura de várias frequências
        ao mesmo tempo. 
        
        Essa transformação é precisa porque o espectro mostra quais frequências
        existem naquele instante e o quão forte cada uma é, isso é importante
        para classificar em qual lane vai cair.
        
        """
        S = np.abs(librosa.stft(y=signal_wave))
        freqs = librosa.fft_frequencies(sr=sample_rate)

        all_freqs = []

        for beat_time in beat_times:
            
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
    
    def load_music(self): 
        """
        Toca a música

        Returns:
            mixer_
        """
        mixer.init()
        mixer.music.load(self.music_path + ".mp3")
        mixer.music.play()
        
        return mixer
    
    def get_qtd_notes(self):
        return self.qtd_notes