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
        
    def draw_line(self):
        pygame.draw.rect(self.screen , self.color_default, self.rect)
             
"""    

"""
