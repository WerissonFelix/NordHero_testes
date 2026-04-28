import pygame
from Game.Config.Game_Config import GameConfig

class NoteManager:
    """ 
    Gerencia a criação, movimentação e colisão de notas musicais no jogo.
    
    Responsável por atualizar posições das notas, detectar acertos do jogador
    e calcular pontuação baseada na precisão do timing.
    """
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
        self.notes_hit = 0
        
    def while_running(self,score, current_time, notes, spawn_offset, screen, keys, keys_pressed):  
        """
        Atualiza posição das notas, detecta colisões e calcula pontuação.
        
        Percorre todas as notas ativas, calcula posição Y baseado no tempo.
        A posição Y atualizar a cada frame do while principal, o que vai dar uma 
        sensação de movimento da nota.
        
        Verifica colisão com teclas e determina precisão do acerto.   
        
        retorna o novo score (se pontuar) e o rating da respectiva nota.
        """
                  
        for note in notes:
            note_time, lane = note

            if note_time - spawn_offset <= current_time:
                """ 
                Atualiza a Y de acordo com o tempo em que a nota aparece na música e o 
                tempo atual que a música está.
                
                O cálculo da speed é feito no GameManager, no método run().
                o Speed é baseado no BPM da música.
                
                o X é fixo, cada note terá o X alinhado com seu respectivo lane.
                """
                
                time_diff = note_time - current_time
                self.y = 400 - (time_diff * self.speed)

                self.x = 200 + lane * 100

                rect = pygame.Rect(self.x, self.y, self.width, self.height)

                pygame.draw.rect(screen, (255, 255, 255),rect)

                if rect.colliderect(keys[lane].rect):
                    if keys_pressed[keys[lane].key]: 
                                                              
                        distance = abs(rect.centery - keys[lane].rect.centery)
                        
                        if distance <= 12:                          
                           self.rating = "Perfect" 
                           score += 100
                        elif 13 <= distance <= 18:
                            self.rating = "Good"
                            score += 50
                        elif distance >= 19:
                            self.rating = "Bad"
                            score += 25     
                        self.notes_hit +=1                     
                        self.notes_to_remove.append(note)
                        
                elif self.y > 600:
                    self.rating = "Miss" 
                    self.notes_to_remove.append(note)
        for n in self.notes_to_remove:
            if n in notes:
                notes.remove(n)
        return score, self.rating

    def get_notes_hit(self):
        return self.notes_hit
   