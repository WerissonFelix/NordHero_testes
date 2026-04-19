import pygame
from Game.Config.Game_Config import GameConfig

class NoteManager:
    def __init__(self,  width, height, color,speed):
        self.width = width
        self.height = height
        self.color = color
        self.handled = True
        self.speed = speed
        self.font = pygame.font.Font(None, 36)
        self.notes_to_remove = []
        
        self.rating = ""
        self.current_rating = ""
        
        self.alpha = 0
        self.col_spd = 5
        self.col_dir = [-1,-1,-1]
        self.def_col = [255,255,255]
        
        self.x = 0
        self.y = 0    
    def while_running(self,score, current_time, notes, spawn_offset, screen, keys, keys_pressed):            
        for note in notes:
            note_time, lane = note

            if note_time - spawn_offset <= current_time:
                time_diff = note_time - current_time
                self.y = 500 - (time_diff * self.speed)

                self.x = 200 + lane * 100

                rect = pygame.Rect(self.x, self.y, self.width, self.height)

                pygame.draw.rect(screen, (200,0,0),rect)

                if rect.colliderect(keys[lane].rect):
                    if keys_pressed[keys[lane].key]: 
                                                              
                        distance = abs(rect.centery - keys[lane].rect.centery)
                        
                        if distance <= 12:                          
                           self.rating = "Perfect" 
                           score += 300
                        elif 13 <= distance <= 18:
                            self.rating = "Good"
                            score += 150
                        elif distance >= 19:
                            self.rating = "Bad"
                            score += 50                          
                        self.notes_to_remove.append(note)
                elif self.y > 600:
                    self.rating = "Miss" 
                    self.notes_to_remove.append(note)
        for n in self.notes_to_remove:
            if n in notes:
                notes.remove(n)
        return score, self.rating
    
    def draw_text(self,rating, screen):
        if rating != "":
            self.current_rating = rating
            self.alpha = 255
        if self.alpha > 0 and self.current_rating != "":
            orig_surf = self.font.render(self.current_rating, True, self.def_col)
            temp_surf = pygame.Surface(orig_surf.get_size(), pygame.SRCALPHA)
            
            temp_surf.set_alpha(self.alpha)
            temp_surf.blit(orig_surf, (0,0))
            
            screen.blit(temp_surf, (10,300))
            self.alpha = max(self.alpha - 4, 0)  
    def effect_text_rating(self):
        mininum = 100
        maximum = 200
        
        for i in range(3):
            self.def_col[i] += self.col_spd * self.col_dir[i]
            
            if self.def_col[i] >= 255:
                col_dir = 0
            elif self.def_col[i] <= 0:
                self.def_col[i] = 255
        