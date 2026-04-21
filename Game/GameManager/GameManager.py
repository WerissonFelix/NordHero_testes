from Game.Config.Game_Config import GameConfig
from Game.Lanes.LaneManager import LaneManager
from Game.Notes.NotesManager import NoteManager
from Game.music.AudioAnalyzer import AudioAnalyzer
from Game.Text.TextManager import TextManager
from Screens.Pause import pause_menu
import pygame, time

class ManageGame:
    def __init__(self, user,music_path):
        pygame.font.init()
        self.user = user
        self.config = GameConfig()
        self.music_path = music_path
        self.textManage  = TextManager()
        self.clock = pygame.time.Clock()
        self.audio = AudioAnalyzer(self.music_path)
        
        self.screen = pygame.display.set_mode(
            (
            self.config.get_screen_width(),
            self.config.get_screen_height()
            )
        )      
        self.font = pygame.font.Font(None, 36)
        self.running = False
        
        self.notes = []
        self.default_lane = [
            
            LaneManager(200,500,(255,0,0), (220,0,0),pygame.K_a),
            LaneManager(300,500,(0,255,0), (0,220,0),pygame.K_s),
            LaneManager(400,500,(0,0,255), (0,0,220),pygame.K_d),
            LaneManager(500,500,(255,255,0), (220,220,0),pygame.K_f),
        ]
        
        self.mixer = None    
        self.count = 4
        self.start_time = time.time()
        
        self.is_paused = False
    def load_to_run(self):  
        """
        
        Carrega todas as notes antes do jogo começar, está
        separado da def run porque este carregamento é pesado 
        e demora alguns segundos para calcular todas as notas
        
        """
        
        self.notes, time = self.audio.Generate_map()
        self.countdown()
    
    def pause_game(self):
        self.mixer.music.pause()
        
        pause_menu(self.user, self.music_path)
        
        self.countdown(True)
        
        self.mixer.music.unpause()
        

    def countdown(self, was_paused = False):  
        time.sleep(2)  
        while self.count >= 0: 
            if self.count >= 0 and time.time() - self.start_time > 1:
                self.count -= 1
                self.start_time = time.time()
            
            text = "GO!" if self.count <= 0 else str(self.count)
            
            self.screen.fill((0, 0, 0))
            
            img = self.font.render(text, True, (255, 255, 255))
            
            self.screen.blit(img, (400,300))
            
            pygame.display.flip()
            
        self.count = 4
        if was_paused == False:
            self.running = True
            self.run()
        
    def run(self):
        score = 0
        self.mixer = self.audio.load_music()
        notesManage = NoteManager(
            self.config.get_note_width(), 
            self.config.get_note_height(),
            (200,0,0),
            self.config.get_base_speed()
        )
        
        while self.running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_game()
                        
            self.screen.fill((0,0,0))
            
            keys_pressed = pygame.key.get_pressed()
            current_time = self.mixer.music.get_pos() / 1000
            
            for key in self.default_lane:
              
                if keys_pressed[key.key]:
                    key.update_line()
                    
                else:
                    key.draw_line()
                   
            score, rating = notesManage.while_running(
                score,
                current_time,self.notes,self.config.get_spawn_offset(),
                self.screen,self.default_lane,
                keys_pressed
            )
            
            color = self.textManage.draw_rating(rating,self.screen)
            self.textManage.effect_text_rating()     
            
            score_text = self.font.render(f"Score: {score}", True, color)    
            self.screen.blit(score_text, (10, 10))
            
            pygame.display.update()
    