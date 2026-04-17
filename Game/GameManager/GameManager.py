from Game.Config.Game_Config import GameConfig
from Game.Lanes.LaneManager import LaneManager
from Game.Notes.NotesManager import NoteManager
from Game.music.AudioAnalyzer import AudioAnalyzer

import pygame
class GameManager:
    
    def __init__(self):
        pygame.font.init()
        self.config = GameConfig()
        self.screen = pygame.display.set_mode((self.config.get_screen_width(), self.config.get_screen_height()))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.running = True
        self.default_lane = [
            
            LaneManager(200,500,(255,0,0), (220,0,0),pygame.K_a),
            LaneManager(300,500,(0,255,0), (0,220,0),pygame.K_s),
            LaneManager(400,500,(0,0,255), (0,0,220),pygame.K_d),
            LaneManager(500,500,(255,255,0), (220,220,0),pygame.K_f),
        ]
        
    def run(self):
        audio = AudioAnalyzer("Game\music\I Thought I Saw Your Face Today - She & Him (Instrumental)")
        notes, time = audio.Generate_map()
        mixer = audio.load_music()
        clock = pygame.time.Clock()
        score = 0
        notesManage = NoteManager(self.config.get_note_width(), self.config.get_note_height(),(200,0,0),self.config.get_base_speed())
        while self.running:
            dt = clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.screen.fill((0,0,0))
            keys_pressed = pygame.key.get_pressed()
            current_time = mixer.music.get_pos() / 1000
            for key in self.default_lane:
                # Verifica se a tecla está pressionada
    
                if keys_pressed[key.key]:
                    key.update_line()
                    
                else:
                    key.draw_line()
                   
            score = notesManage.while_running(score, current_time,notes,self.config.get_spawn_offset(),self.screen,self.default_lane, keys_pressed)

            score_text = self.font.render(f"Score: {score}", True, (255,255,255))
            print(score)
            self.screen.blit(score_text, (10, 10))
            pygame.display.update()

testee = GameManager()
testee.run()