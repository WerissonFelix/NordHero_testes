from Game.Config.Game_Config import GameConfig
from Game.Lanes.LaneManager import LaneManager
from Game.Notes.NotesManager import NoteManager
from Game.music.AudioAnalyzer import AudioAnalyzer
from Game.Text.TextManager import TextManager
from Game.Bar.BarProgress import BarProgressManager
from Game.Bar.SongProgressBar import SongProgressBar
from Game.Bar.BarEvents import BarEvents
from Game.Bar.lifeBarManager import LifeBarManager

from DataBase.repositories.xp_repository import XpRepository
from DataBase.repositories.song_repository import SongRepository

from Screens.Pause import pause_menu
from Screens.Match_summary import match_summary
import pygame, time, os
class ManageGame:
    """
    Controlador principal do jogo de ritmo.
    
    Gerencia o fluxo completo da partida: carregamento, contagem regressiva,
    execução do jogo com detecção de notas, pausa e tela de resultado final.
    """
    def __init__(self, user, music_path, mod, multiplicador=1,second_music_path=None, tipo_2players= None, full_music_path = None, phase_number = None ):
        pygame.font.init()
        self.user = user
        self.config = GameConfig()
        self.music_path = music_path
        self.second_music_path = second_music_path
        self.full_music_path = full_music_path
        self.tipo_2players = tipo_2players
        self.multiplicador = multiplicador
        self.textManage  = TextManager(mod)
        self.clock = pygame.time.Clock()
        current_dir = os.path.dirname(__file__)
        songRepository = SongRepository()
        self.song = songRepository.get_by_file_path(self.music_path)
        self.mod = mod
        self.phase_number = phase_number
        self.notesManage = None        
        if mod == "Single Player":  
            self.width = self.config.get_screen_width()
            self.height = self.config.get_screen_height()
            self.audio = AudioAnalyzer(self.music_path, self.mod)
            bg_path = os.path.join(current_dir, "..", "..", "Images", "TelaSinglePlayer.png")  
        else:
            print(mod)
            self.width = 1280
            self.height = 720
            
            if tipo_2players == "Contra":
                self.audio = AudioAnalyzer(self.music_path, self.mod, self.second_music_path)
                bg_path = os.path.join(current_dir, "..", "..", "Images", "TelaVersus.png")
            else:
                self.audio = AudioAnalyzer(self.music_path, self.mod, self.second_music_path, self.full_music_path)
                bg_path = os.path.join(current_dir, "..", "..", "Images", "TelaCoop.png") 
        self.screen = pygame.display.set_mode(
            (
            self.width,
            self.height
            )
        )
        self.font = pygame.font.Font(None, 36)
        duration_music = self.audio.get_duration()
        bar_w = 300
        bar_x = (self.width - bar_w) // 2 if mod == "Single Player" else ((self.width - bar_w) // 2) - 50
        
        self.song_progress_bar = SongProgressBar(x=bar_x, y=10, width=bar_w, height=14, duration_ms = duration_music, font= self.font)
        self.background = pygame.image.load(bg_path)

        self.background = pygame.transform.scale(
            self.background,
            (self.width, self.height)
        )
        self.running = False
        self.notes = []
        self.base_bpm = 120
        self.bpm = 0
        self.default_lane = [
            
            LaneManager(180,500, (255,0,0), (220,0,0), self.config.key1, self.width, self.height),
            LaneManager(280,500, (0,255,0), (0,220,0), self.config.key2, self.width, self.height),
            LaneManager(380,500, (0,0,255), (0,0,220), self.config.key3, self.width, self.height),
            LaneManager(480,500, (255,255,0), (220,220,0), self.config.key4, self.width, self.height),    
           
        ]
        if self.mod == "2 Players":
            self.default_lane.append(LaneManager(780, 500, (255,0,0), (220,0,0), self.config.key5, self.width, self.height))
            self.default_lane.append(LaneManager(880, 500, (0,255,0), (0,220,0), self.config.key6, self.width, self.height))
            self.default_lane.append(LaneManager(980, 500, (0,0,255), (0,0,220), self.config.key7, self.width, self.height))
            self.default_lane.append(LaneManager(1080, 500, (255,255,0), (220,220,0), self.config.key8, self.width, self.height))
        
        self.mixer = None    
        self.count = 4
        self.start_time = time.time()
        self.count_to_load = -1
        self.is_paused = False
        
    def load_to_run(self):    
        """
        Carrega todas as notes antes do jogo começar, está
        separado do método run() porque este carregamento é pesado 
        e demora alguns segundos para calcular todas as notas
        """  
        text = "Loading"
        time.sleep(2)
        while self.count_to_load < 4:
            if self.count_to_load < 4 and time.time() - self.start_time > 1:
                self.count_to_load += 1
                self.start_time = time.time()
                
                text += " ."
            
            if self.count_to_load == 4:
                text = "Please, wait"
            
            self.screen.fill((0, 0, 0))
                
            img = self.font.render(text, True, (255, 255, 255))
        
            img_rect = img.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            
            self.screen.blit(img, img_rect )
            
            pygame.display.flip()
        else:
            self.notes, self.bpm = self.audio.Generate_map()
            self.countdown()
    
    def pause_game(self, total_notes, notes_hit, score):
        """
        
        Pausa a música e exibe o menu de pausa.
        
        """
        self.mixer.music.pause()
        
        pause_menu(self.user, self.music_path, total_notes, notes_hit, score, self.tipo_2players, None, self.config, self.mod)
        
        self.default_lane = [
    
            LaneManager(180,500, (255,0,0), (220,0,0), self.config.key1, self.width, self.height),
            LaneManager(280,500, (0,255,0), (0,220,0), self.config.key2, self.width, self.height),
            LaneManager(380,500, (0,0,255), (0,0,220), self.config.key3, self.width, self.height),
            LaneManager(480,500, (255,255,0), (220,220,0), self.config.key4, self.width, self.height),
        ]
        
        if self.mod == "2 Players":
            self.default_lane.append(  
                LaneManager(780, 500, (255,0,0), (220,0,0), self.config.key5, self.width, self.height))
            self.default_lane.append(
                LaneManager(880, 500, (0,255,0), (0,220,0), self.config.key6, self.width, self.height))
            self.default_lane.append(
                LaneManager(980, 500, (0,0,255), (0,0,220), self.config.key7, self.width, self.height))
            self.default_lane.append(
                LaneManager(1080, 500, (255,255,0), (220,220,0), self.config.key8, self.width, self.height))
        
        self.countdown(True)
        
        self.mixer.music.unpause()
        
    def countdown(self, was_paused = False):  
        """
        Exibe contagem regressiva (3, 2, 1, GO!) antes de iniciar.
        """
        time.sleep(2)  
        while self.count >= 0: 
            if self.count >= 0 and time.time() - self.start_time > 1:
                self.count -= 1
                self.start_time = time.time()
            
            text = "GO!" if self.count <= 0 else str(self.count)
            
            self.screen.fill((0, 0, 0))
            
            img = self.font.render(text, True, (255, 255, 255))
            
            img_rect = img.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            
            self.screen.blit(img, img_rect )
        
            pygame.display.flip()
            
        self.count = 4
        if was_paused == False:
            self.running = True
            self.run()
        
    def run(self):
        """
        
        Loop principal do jogo de ritmo.
        
        """
        self.score = [0, 0]
        self.index_player = 0
        self.mixer = self.audio.load_music()
        self.current_time = self.mixer.music.get_pos() / 1000

        MUSIC_END_EVENT = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(MUSIC_END_EVENT)
        
        speed_multiplier = self.bpm / self.base_bpm if self.bpm > 0 else 1.0
        
        min_speed = 0.5  
        max_speed = 2.0    
        
        speed_multiplier = max(min_speed, min(speed_multiplier, max_speed))
        
        adjusted_speed = self.config.get_base_speed() / speed_multiplier
        
        if self.multiplicador == 0:     
            adjusted_speed *= 0.8
        elif self.multiplicador == 2:    
            adjusted_speed *= 1.5
            
        self.notesManage = NoteManager(
            self.config.get_note_width(), 
            self.config.get_note_height(),
            (255, 255, 255),
            adjusted_speed,
            self.mod,
            self.tipo_2players,
            self.textManage
        )
        
        keys = [
            pygame.key.name(self.config.key1),
            pygame.key.name(self.config.key2),
            pygame.key.name(self.config.key3),
            pygame.key.name(self.config.key4),
        ]

        if self.mod == "2 Players":
            keys.extend([
                pygame.key.name(self.config.key5),
                pygame.key.name(self.config.key6),
                pygame.key.name(self.config.key7),
                pygame.key.name(self.config.key8),
            ])

            barEvent = BarEvents(self.screen, self.mod, self.textManage) 
            
            if self.tipo_2players == "Contra":
                callback1 = lambda: barEvent.penalty_loss_points_enemy(1, self.score, self.notesManage.rating)
                callback2 = lambda: barEvent.penalty_loss_points_enemy(0, self.score, self.notesManage.rating)
                     
                self.bar_p1 = BarProgressManager(300, 600, 200, 20, 20, callback1)
                self.bar_p2 = BarProgressManager(900, 600, 200, 20, 20, callback2)
            else:    
                callback_pun1 = lambda: barEvent.penalty_loss_points_both(0, self.score, self.notesManage.rating)    
                callback_pun2 = lambda: barEvent.penalty_loss_points_both(1, self.score, self.notesManage.rating)    
                self.bar_pun_p1 = BarProgressManager(230, 620, 200, 20, 20, callback_pun1)
                self.bar_pun_p2 = BarProgressManager(830, 620, 200, 20, 20, callback_pun2)
 
                self.bar_rain_p1 = BarProgressManager(617, 260, 20, 200, 20, None)
                self.bar_rain_p2 = BarProgressManager(643, 260, 20, 200, 20, None)
                
                def on_both_full():
                    self.notesManage.spawn_rainbow_notes(self.notes, 0, self.current_time)
                    self.notesManage.spawn_rainbow_notes(self.notes, 1, self.current_time)
                    if self.textManage:
                        self.textManage.add_notification(
                            "RAINBOW NOTES!", (480, 80), (255, 200, 0), duration_frames=180
                        )

                self.bar_rain_p1.set_partner(self.bar_rain_p2, on_both_full)
                self.bar_rain_p2.set_partner(self.bar_rain_p1, on_both_full)
        else:
            if self.song.story_difficulty_id == 1:
                self.current_hearts = 7
                heart_x = 240
            elif self.song.story_difficulty_id == 2:
                self.current_hearts = 5
                heart_x = 280
            else:
                self.current_hearts = 3
                heart_x = 315

            self.life_bar = LifeBarManager(x=heart_x, y=550, max_lives=self.current_hearts, heart_size=36,gap=12,on_game_over=self.game_over)
        """ 
        Loop principal do jogo.
    
        Inicializa música, calcula velocidade baseada no BPM da música,
        processa entrada/tecla pressionada do jogador, atualiza notas e renderiza
        feedback visual (score, ratings, lanes) a 60 FPS.
        """
        self.keys_pressed = [] 
        while self.running:
                     
            self.current_time = self.clock.tick(60) / 1000
            self.song_progress_bar.update(self.mixer.music.get_pos())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_game(self.audio.get_qtd_notes(),self.notesManage.get_notes_hit(), self.score)
                         
                        keys = [
                            pygame.key.name(self.config.key1),
                            pygame.key.name(self.config.key2),
                            pygame.key.name(self.config.key3),
                            pygame.key.name(self.config.key4),
                        ]

                        if self.mod == "2 Players":
                            keys.extend([
                                pygame.key.name(self.config.key5),
                                pygame.key.name(self.config.key6),
                                pygame.key.name(self.config.key7),
                                pygame.key.name(self.config.key8),
                            ])
                    else:
                        for key in self.default_lane:
                            if event.key == key.key:
                                self.keys_pressed.append(key)
                                key.update_line()
                if event.type == pygame.KEYUP:
                    for key in self.default_lane:
                        if event.key == key.key:
                            try:
                                self.keys_pressed.remove(key)
                            except ValueError:
                                pass
                            key.update_line()
                elif event.type == MUSIC_END_EVENT:
                    xpRepository = XpRepository()
                    xpRepository.complete_phase(self.user.id,self.song.story_difficulty_id, self.song.id, self.phase_number)
                    self.end_match(self.audio.get_qtd_notes(), self.notesManage.get_notes_hit())
                        
            self.screen.blit(self.background, (0, 0))
           
            keys_held = pygame.key.get_pressed()
            for key in self.default_lane:
                if keys_held[key.key]:
                    key.update_line()
                else:
                    key.draw_line()
                
            self.current_time = self.mixer.music.get_pos() / 1000
            
            for i, key in enumerate(keys):
                text = self.font.render(key, True, (255, 255, 255))
                
                if i < 4:
                    x = 220 + (i * 100)

                else:
                    x = 820 + ((i - 4) * 100)

                y = 520

                self.screen.blit(text, (x, y))
        
            self.score, rating, combo, extra, self.keys_pressed, self.index_player = self.notesManage.while_running(
                self.score,
                self.current_time,self.notes,self.config.get_spawn_offset(),
                self.screen,self.default_lane,
                self.keys_pressed,
                keys_held
            )
            
            color = self.textManage.update(self.screen, combo, extra)

            if self.mod == "2 Players":
                if self.tipo_2players == "Contra":
                    score_text_p1 = self.font.render(
                        f"P1: {self.score[0]}",
                        True,
                        (255, 255, 0)
                    )

                    score_text_p2 = self.font.render(
                        f"P2: {self.score[1]}",
                        True,
                        (255, 255, 0)
                    )

                    self.screen.blit(score_text_p1, (10, 10))
                    self.screen.blit(score_text_p2, (750, 10))
                    
                elif self.tipo_2players == "Juntos":
            
                    score_text = self.font.render(
                        f"Score: {sum(self.score)}",
                        True,
                        (255, 255, 0)
                    )
                    self.screen.blit(score_text, (10, 10))
                if self.tipo_2players == "Contra":
                    self.bar_p1.draw(self.screen)
                    self.bar_p2.draw(self.screen)
                else:
                    self.bar_pun_p1.draw(self.screen)
                    self.bar_pun_p2.draw(self.screen)
                    self.bar_rain_p1.draw(self.screen)
                    self.bar_rain_p2.draw(self.screen)
            else:
                score_text = self.font.render(
                    f"Score: {self.score[0]}",
                    True,
                    (255, 255, 0)
                )
                self.life_bar.draw(self.screen)
                self.screen.blit(score_text, (10, 10))
                
            for k,v in enumerate(rating):
                if v != "":
                    self.textManage.draw_rating(rating, k)
                    
                if v == "Perfect" and self.tipo_2players == "Contra":
                    self.bar_p1.add_perfect()  if k == 0 else self.bar_p2.add_perfect()  
                    
                if self.tipo_2players == "Juntos":
                    if v == "Perfect":
                        self.bar_rain_p1.add_perfect() if k == 0 else self.bar_rain_p2.add_perfect()
                    if v in ["Miss", "Bad"]:
                        self.bar_pun_p1.add_bad_miss(k, rating) if k == 0 else self.bar_pun_p2.add_bad_miss(k, rating)
                
                if self.mod == "Single Player":
                    self.life_bar.handle_rating(v)
            self.song_progress_bar.draw(self.screen) 
            
            if self.mod == "Single Player":
                self.life_bar.update(self.current_time)                       
                
            pygame.display.update()
            
    def game_over(self):        
        self.mixer.music.pause()
        time.sleep(2)
        match_summary(self.user, self.audio.get_qtd_notes(), self.notesManage.get_notes_hit(), self.music_path, self.score, self.tipo_2players, "GAME OVER!")
        
    def end_match(self, total_notes, notes_hit):        
        time.sleep(2)
        match_summary(self.user, total_notes, notes_hit, self.music_path, self.score, self.tipo_2players)