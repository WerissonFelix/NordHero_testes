import pygame

class LaneManager:
    def __init__(self, x, y, color_default, color_pressed, key):
        self.x = x
        self.y = y
        self.screen = pygame.display.set_mode((800,600))
        self.color_default = color_default
        self.color_pressed = color_pressed
        self.key = key
        self.rect = pygame.Rect(self.x, self.y, 100, 20)
        self.active = True
    
    def update_line(self):
        pygame.draw.rect(self.screen , self.color_pressed, self.rect)
        
    def draw_all_lines(self):
        pygame.draw.rect(self.screen , self.color_default, self.rect)
             
"""    
keys = [
    LaneManager(200,500,(255,0,0), (220,0,0),pygame.K_a),
    LaneManager(300,500,(0,255,0), (0,220,0),pygame.K_s),
    LaneManager(400,500,(0,0,255), (0,0,220),pygame.K_d),
    LaneManager(500,500,(255,255,0), (220,220,0),pygame.K_f),
]
"""
