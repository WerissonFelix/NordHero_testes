import pygame
from Game.Config.Game_Config import GameConfig

class NoteManager:
    """ 
    Gerencia a criação, movimentação e colisão de notas musicais no jogo.
    
    Responsável por atualizar posições das notas, detectar acertos do jogador
    e calcular pontuação baseada na precisão do timing.
    """
    def __init__(self,  width, height, color, speed, mod):
        self.width = width
        self.height = height
        self.color = color
        self.handled = True
        self.speed = speed
        self.mod = mod
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
        
        num_players = 1 if self.mod == "Single Player" else 2
        
        self.notes_hit = [
            {"Miss": 0, "Bad": 0, "Good": 0, "Perfect": 0}
            for _ in range(num_players)
            ]
     
        self.combo = 0
        self.extra_score = 0
        self.active_long_notes = []
        
    def while_running(self, score, current_time, notes, spawn_offset, screen, keys, keys_pressed, keys_held):  
        """
        Atualiza posição das notas, detecta colisões e calcula pontuação.
        
        Percorre todas as notas ativas, calcula posição Y baseado no tempo.
        A posição Y atualizar a cada frame do while principal, o que vai dar uma 
        sensação de movimento da nota.
        
        Verifica colisão com teclas e determina precisão do acerto.   
        
        retorna o novo score (se pontuar) e o rating da respectiva nota.
        """          
        for note in notes:
            note_time = note[0]
            lane = note[1]
            index = 0 if 0 <= lane < 4 else 1
            duracao =  note[3] if len(note) > 3 else 0
            
            limite = 600 if self.mod == "Single Player" else 720
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

                if lane >= 4:
                    self.x = 800 + (lane - 4)  * 100
                else:
                    self.x = 200 + lane * 100 

                altura_base = self.height
                if duracao > 0:
                    altura_real = self.height + (duracao * self.speed)
                    rect_y = self.y - (altura_real - self.height) 
                    
                    rect = pygame.Rect(self.x, rect_y, self.width, altura_real)
                    
                    bottom_y = self.y + self.height
                    
                    start_hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
                                                   
                    if note in self.active_long_notes:
                        bottom_y = keys[lane].rect.centery
                        
                    draw_height = bottom_y - rect_y
                    
                    if draw_height > 0:
                        rect_draw = pygame.Rect(self.x, rect_y, self.width, draw_height)
                        pygame.draw.rect(screen, (255, 255, 255), rect_draw)
                else:
                    altura_real = altura_base
                    rect_y = self.y
                    rect = pygame.Rect(self.x, rect_y, self.width, altura_real)
                    pygame.draw.rect(screen, (255, 255, 255), rect)    
                    
                if rect.colliderect(keys[lane].rect):        
            
                    just_pressed = keys[lane] in keys_pressed
                    
                    is_held_down = keys_held[keys[lane].key]
                    
                    if duracao > 0:
                        if is_held_down and note not in self.active_long_notes:
                            self.active_long_notes.append(note)
                            
                        elif note in self.active_long_notes: 
                            if is_held_down:
                                if start_hitbox.colliderect(keys[lane].rect):
                                    distance = abs(start_hitbox.centery - keys[lane].rect.centery)     
                                    is_held_down = keys_held[keys[lane].key]
                                    
                                    self.create_rating(distance, score, index)
                                    
                                if rect_y >= keys[lane].rect.centery:
                                    self.notes_to_remove.append(note)
                                    self.active_long_notes.remove(note)
                            else:
                                self.rating = "Miss"
                                self.notes_hit[index]["Miss"] += 1
                                self.combo = 0
                                self.notes_to_remove.append(note)
                                self.active_long_notes.remove(note)
                    else: 
                        if just_pressed:   
                            distance = abs(rect.centery - keys[lane].rect.centery) 
                                                       
                            score = self.create_rating(distance, score, index)
                                           
                            self.notes_to_remove.append(note)
                            try:
                                keys_pressed.remove(keys[lane])
                            except ValueError:
                                pass
                elif rect_y > limite:
                    self.rating = "Miss" 
                    self.notes_hit[index]["Miss"] += 1
                    self.combo = self.extra_score = 0
                    self.notes_to_remove.append(note)
                    
        for n in self.notes_to_remove:
            if n in notes:
                notes.remove(n)
        self.notes_to_remove.clear()
                
        return score, self.rating, self.combo, self.extra_score, keys_pressed

    def create_rating(self, distance, score, index):
        """Cria texto de avaliação ("Bad", "Good", "Perfect")"""     
        if distance <= 12:
            self.rating = "Perfect" 
            score += 100
            self.notes_hit[index]["Perfect"] += 1
            self.combo += 1
            self.extra_score = 0
            if  1 < self.combo <= 5 :   
                self.extra_score = 5
            elif 5 < self.combo <= 10:
                self.extra_score = 10
            elif 10 < self.combo <= 20:
                self.extra_score = 15 
            else:
                self.extra_score = 20
            score += self.extra_score     
        elif 13 <= distance <= 18:
            self.rating = "Good"
            score += 50
            self.combo = self.extra_score = 0
            self.notes_hit[index]["Good"] += 1
        elif distance >= 19:
            self.rating = "Bad"
            score += 25 
            self.combo = self.extra_score = 0
            self.notes_hit[index]["Bad"] += 1
        return score
    
    def get_notes_hit(self):
        return self.notes_hit
    