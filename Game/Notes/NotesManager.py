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
        self.def_col = [255,255,0]
        
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

   