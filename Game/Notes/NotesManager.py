import pygame
from Game.Config.Game_Config import GameConfig

class NoteManager:
    def __init__(self, beat_time, lane_index, x_position, width, height, color):
        self.beat_time = beat_time
        self.lane_index = lane_index
        
        self.width = width
        self.height = height
        self.color = color
        
        self.rect = pygame.Rect(x_position, 0, width, height)
        
    def update(self, current_time, speed, target_y, screen_height):
        if not self.active: 
            return
        
        time_diff = self.beat_time - current_time
        self.rect.y = target_y - (time_diff * speed)
        
        if self.rect.y > screen_height + 100:
            self.active = False
        
    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, self.color, self.rect)
        