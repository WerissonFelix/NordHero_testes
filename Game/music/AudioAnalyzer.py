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


    def __init__(self, music_path, mod, second_music_path=None):
        self.music_path = music_path
        self.second_music_path = second_music_path
        self.notes = []
        self.qtd_notes = 0
        self.time =  120 # Fallback
        
        self.mod = mod
        
        self.times = []
        self.lanes = []
        
        self.limite = 0
        if self.mod == "Single Player":
            self.lanes_notes = {0: [], 1: [], 2: [], 3: []}
            self.limite = 1
            
        else:
            self.lanes_notes = {
                0: [], 1: [], 2: [], 3: [], 
                4: [], 5: [], 6: [], 7: []
            }
            self.limite = 2
            self.notes_song2 = []
        
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
        
        for i in range(self.limite):
            if i == 0:
                signal_wave, sample_rate = librosa.load(self.music_path)
            else:
                print(self.second_music_path)
                signal_wave, sample_rate = librosa.load(self.second_music_path)
            # librosa.load retorna: um numpy array e um int, sendo, respectivamente, o nome das variáveis

            time, beat_frames = librosa.beat.beat_track(y=signal_wave, sr=sample_rate)
            beat_times = librosa.frames_to_time(beat_frames, sr=sample_rate)
            time = float(np.squeeze(time))

            # Esse frames_to_time é para obtermos o tempo real de cada beat que o beat_track achou
            # o squeeze é usado para garantir que time seja um float
            
            self.qtd_notes += len(beat_times)
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

                    set_lane = 0 if i == 0 else 4
                    
                    if freq < percentiles[0]:
                        lane = 0 + set_lane
                        self.lanes_notes[lane].append(beat_time)
                    elif freq < percentiles[1]:
                        lane = 1 + set_lane
                        self.lanes_notes[lane].append(beat_time)
                    elif freq < percentiles[2]:
                        lane = 2 + set_lane
                        self.lanes_notes[lane].append(beat_time)
                    else:
                        lane = 3 + set_lane
                        self.lanes_notes[lane].append(beat_time)
            
        self.verify_for_long_notes()
        return self.notes, self.time
    
    def verify_for_long_notes(self):
        """ 
        Verifica se existem notas muito próximas, agrupando-as em notas longas.
        Padroniza o array de notas final para evitar conflitos de variáveis.
        """
        
        for lane, times in self.lanes_notes.items():
            if not times:
                continue
            
            sequencia = [times[0]]
            
            for i in range(1,len(times)):
                tempo_atual = times[i]
                tempo_anterior = sequencia[-1]
                       
                if tempo_atual - tempo_anterior < 0.5:
                    sequencia.append(tempo_atual)
                else:
                    if len(sequencia) > 4:
                        duracao = abs(sequencia[-1] - sequencia[0])
                        self.notes.append([sequencia[0], lane, len(sequencia), duracao])
                    else:
                        for t in sequencia:
                            self.notes.append([t, lane, 1])
                    sequencia = [tempo_atual]
                        
                if tempo_atual == times[-1]:
                    if len(sequencia) > 4:
                        duracao = abs(sequencia[-1] - sequencia[0])
                        self.notes.append([sequencia[0], lane, len(sequencia), duracao])
                    else:
                        for t in sequencia:
                            self.notes.append([t, lane, 1])  
            self.notes.sort(key=lambda x: x[0])
    def load_music(self): 
        """
        Toca a música

        Returns:
            mixer_
        """
        mixer.init()
        mixer.music.load(self.music_path)
        mixer.music.play()
        
        return mixer
    
    def get_qtd_notes(self):
        return self.qtd_notes