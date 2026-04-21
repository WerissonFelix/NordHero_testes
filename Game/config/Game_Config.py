
class GameConfig:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.FPS = 60
        self.BASE_SPEED = 300
        self.SPAWN_OFFSET = 1.5
    
        self.LANE_WIDTH = 100
        self.HIT_ZONE_HEIGHT = 40
        self.NOTE_WIDTH = 50
        self.NOTE_HEIGHT = 25

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
    
    def set_screen_width(self, value):
        if value <= 0:
            raise ValueError("screen_width deve ser positivo")
        self.screen_width = value
    
    def set_screen_height(self, value):
        if value <= 0:
            raise ValueError("screen_height deve ser positivo")
        self.screen_heigh = value