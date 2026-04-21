import pygame

class TextManager:
    def __init__(self):        
        self.alpha = 0
        self.font = pygame.font.Font(None, 36)
        self.col_spd = 5
        self.col_dir = [-1,-1,-1]
        self.def_col = [255,255,0]
        self.current_message = ""     
        self.rainbow = [
            (255, 255, 255),
            (255, 0, 0),
            (255, 128, 0),
            (255, 255, 0),
            (128, 255, 0),
            (0, 255, 0),
            (0, 255, 128),
            (0, 255, 255),
            (0, 128, 255),
            (0, 0, 255),
            (127, 0, 255),
            (255, 0, 255),
            (255, 0, 127),
            (128, 128, 128)
        ]    
        
        self.rainbow_index = 0
        self.rainbow_speed = 0.1
        self.rainbow_change = 0
        self.color = (255,255,255)    
    def draw_rating(self, rating, screen):
        if rating != "":
            self.current_message = rating
            self.alpha = 255
        if self.alpha > 0 and self.current_message != "":
            if self.current_message == "Bad":
                self.color = self.rainbow[1]
            elif self.current_message == "Good":
                self.color = self.rainbow[5]
            elif self.current_message == "Perfect":
                self.color = self.rainbow_effect()
            else: 
                self.color = self.rainbow[-1]
                
            orig_surf = self.font.render(self.current_message, True, self.color)
            temp_surf = pygame.Surface(orig_surf.get_size(), pygame.SRCALPHA)
            
            temp_surf.set_alpha(self.alpha)
            temp_surf.blit(orig_surf, (0,0))
            
            screen.blit(temp_surf, (10,300))
            self.alpha = max(self.alpha - 4, 0)  
        return self.color
    def effect_text_rating(self):    
        for i in range(3):
            self.def_col[i] += self.col_spd * self.col_dir[i]
            
            if self.def_col[i] >= 255:
                self.col_dir = 0
            elif self.def_col[i] <= 0:
                self.def_col[i] = 255
    def rainbow_effect(self):
        self.rainbow_change += self.rainbow_speed
        
        if self.rainbow_change > 1:
            self.rainbow_change = 0
            
            self.rainbow_index += 1
            
            if self.rainbow_index > 13:
                self.rainbow_index = 0        
        return self.rainbow[self.rainbow_index]