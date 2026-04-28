from Game.Config.Game_Config import GameConfig
from Game.Lanes.LaneManager import LaneManager
from Game.Notes.NotesManager import NoteManager
from Game.music.AudioAnalyzer import AudioAnalyzer
from Game.Text.TextManager import TextManager
from Screens.Pause import pause_menu
from Screens.Match_summary import match_summary
import pygame, time, os

class ManageGame:
    """
    Controlador principal do jogo de ritmo.
    
    Gerencia o fluxo completo da partida: carregamento, contagem regressiva,
    execução do jogo com detecção de notas, pausa e tela de resultado final.
    """
    def __init__(self, user,music_path):
        pygame.font.init()
        self.user = user
        self.config = GameConfig()
        self.music_path = music_path
        self.textManage  = TextManager()
        self.clock = pygame.time.Clock()
        current_dir = os.path.dirname(__file__)
        bg_path = os.path.join(current_dir, "..", "..", "Images", "telainicial.png")
        self.background = pygame.image.load(bg_path)

        self.background = pygame.transform.scale(
            self.background,
            (self.config.get_screen_width(), self.config.get_screen_height())
        )
        
        self.audio = AudioAnalyzer(self.music_path)
        self.notesManage = None
        self.screen = pygame.display.set_mode(
            (
            self.config.get_screen_width(),
            self.config.get_screen_height()
            )
        )      
        self.font = pygame.font.Font(None, 36)
        self.running = False
        
        self.notes = []
        self.base_bpm = 120
        self.bpm = 0
        
        self.default_lane = [
            
            LaneManager(180,500,(255,0,0), (220,0,0),pygame.K_a),
            LaneManager(280,500,(0,255,0), (0,220,0),pygame.K_s),
            LaneManager(380,500,(0,0,255), (0,0,220),pygame.K_d),
            LaneManager(480,500,(255,255,0), (220,220,0),pygame.K_f),
        ]
        
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
            
            self.screen.blit(img, (350,300))
            
            pygame.display.flip()                
        else:
            self.notes, self.bpm = self.audio.Generate_map()
            self.countdown()
    
    def pause_game(self, total_notes, notes_hit):
        """
        
        Pausa a música e exibe o menu de pausa.
        
        """
        self.mixer.music.pause()
        
        pause_menu(self.user, self.music_path, total_notes, notes_hit)
        
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
            
            self.screen.blit(img, (350,300))
            
            pygame.display.flip()
            
        self.count = 4
        if was_paused == False:
            self.running = True
            self.run()
        
    def run(self):
        """
        
        Loop principal do jogo de ritmo.
        
        """
        
        score = 0
        self.mixer = self.audio.load_music()
        
        MUSIC_END_EVENT = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(MUSIC_END_EVENT)
        
        speed_multiplier = self.bpm / self.base_bpm if self.bpm > 0 else 1.0
        
        min_speed = 0.5  
        max_speed = 2.0    
        
        speed_multiplier = max(min_speed, min(speed_multiplier, max_speed))
        
        adjusted_speed = self.config.get_base_speed() / speed_multiplier
        
        self.notesManage = NoteManager(
            self.config.get_note_width(), 
            self.config.get_note_height(),
            (255, 255, 255),
            adjusted_speed
        )
        
        """ 
        Loop principal do jogo.
    
        Inicializa música, calcula velocidade baseada no BPM da música,
        processa entrada/tecla pressionada do jogador, atualiza notas e renderiza
        feedback visual (score, ratings, lanes) a 60 FPS.
        """
        
        while self.running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_game(self.audio.get_qtd_notes(),self.notesManage.get_notes_hit())
                elif event.type == MUSIC_END_EVENT:
                    self.end_match(self.audio.get_qtd_notes(),self.notesManage.get_notes_hit())
                        
            self.screen.blit(self.background, (0, 0))
            
            keys_pressed = pygame.key.get_pressed()
            current_time = self.mixer.music.get_pos() / 1000
            
            for key in self.default_lane:
              
                if keys_pressed[key.key]:
                    key.update_line()
                    
                else:
                    key.draw_line()
            
            key_a = self.font.render("a", True, ((255, 255, 255)))    
            key_s = self.font.render("s", True, ((255, 255, 255)))
            key_d = self.font.render("d", True, ((255, 255, 255)))    
            key_f = self.font.render("f", True, ((255, 255, 255)))    
            
            self.screen.blit(key_a, (220, 520))
            self.screen.blit(key_s, (320, 520))
            self.screen.blit(key_d, (420, 520))
            self.screen.blit(key_f, (520, 520))
        
            score, rating = self.notesManage.while_running(
                score,
                current_time,self.notes,self.config.get_spawn_offset(),
                self.screen,self.default_lane,
                keys_pressed
            )
            
            color = self.textManage.draw_rating(rating,self.screen)
            self.textManage.effect_text_rating()     
            
            score_text = self.font.render(f"Score: {score}", True, ((255, 255, 0)))    
            self.screen.blit(score_text, (10, 10))
            
            pygame.display.update()
    
    def end_match(self, total_notes, notes_hit):        
        time.sleep(2)
        match_summary(self.user, total_notes, notes_hit)
    # fazer uma def resume_party que mostra os resultados da partida, só chama se
    # o jogador quitar ou for até ao fim
    # se quitar, volta pra home
    # até o fim, volta pro choice_music
    # mostra o Rank do jogador com base na porcentagem de acerto
    # tentar mostrar quantos miss, goods, perfects (opcional) no final