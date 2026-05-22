import pygame

class GameConfig:
    """
    Classe que contém as principais configurações para o jogo funcionar.
    Seus métodos consistem em retornar suas instâncias para que outras classes/defs possam 
    usar.
    """    
    
    def __init__(self):
        self.key1 = pygame.K_a
        self.key2 = pygame.K_s
        self.key3 = pygame.K_d
        self.key4 = pygame.K_f 
        
        self.screen_width = 800
        self.screen_height = 600
        self.FPS = 60
        self.BASE_SPEED = 300
        self.SPAWN_OFFSET = 1.5
    
        self.LANE_WIDTH = 100
        self.HIT_ZONE_HEIGHT = 40
        self.NOTE_WIDTH = 50
        self.NOTE_HEIGHT = 25

    """
    
    Cada def que tenha um get_ no nome retornará seus respectivos valores das variáveis,
    
    """
    def get_screen_width(self):
        return self.screen_width
    
    def get_screen_height(self):
        return self.screen_height
    
    def get_fps(self):
        return self.FPS
    
    def get_base_speed(self):
        return self.BASE_SPEED
    
    def get_spawn_offset(self):
        return self.SPAWN_OFFSET
    
    def get_lane_width(self):
        return self.LANE_WIDTH
    
    def get_hit_zone_height(self):
        return self.HIT_ZONE_HEIGHT
    
    def get_note_width(self):
        return self.NOTE_WIDTH
    
    def get_note_height(self):
        return self.NOTE_HEIGHT
    
    """
    
    Cada def que tiver um set_ no seu nome, atualizará o default da respectiva variável
    da class GameConfig, pra essas é necessário passar um valor como parâmetro.
    
    """
    
    def set_screen_width(self, value):
        if value <= 0:
            raise ValueError("screen_width deve ser positivo")
        self.screen_width = value
    
    def set_screen_height(self, value):
        if value <= 0:
            raise ValueError("screen_height deve ser positivo")
        self.screen_heigh = value