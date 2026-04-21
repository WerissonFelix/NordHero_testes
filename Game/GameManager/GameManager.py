from Game.Config.Game_Config import GameConfig
from Game.Lanes.LaneManager import LaneManager
from Game.Notes.NotesManager import NoteManager
from Game.music.AudioAnalyzer import AudioAnalyzer
from Game.Text.TextManager import TextManager
import pygame

class ManageGame:
    
    def __init__(self):
        pygame.font.init()
        self.config = GameConfig()
        self.textManage  = TextManager()
        self.clock = pygame.time.Clock()
        self.audio = AudioAnalyzer("Game\music\I Thought I Saw Your Face Today - She & Him (Instrumental)")
        
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
    def load_to_run(self):  
        self.notes, time = self.audio.Generate_map()
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