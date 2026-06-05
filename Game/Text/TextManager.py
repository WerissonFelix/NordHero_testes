import pygame

class TextManager:
    """
    Gerencia exibição de textos de feedback com efeitos visuais e fade-out.
    
    """
    def __init__(self, mod):        
        """
        Inicializa transparência, fonte, paleta de cores e estado inicial.
        
        """
        self.mod = mod
        self.font = pygame.font.Font(None, 36)
        self.col_spd = 5
        self.col_dir = [-1,-1,-1]
        self.def_col = [255,255,0]
        self.current_message = ["", ""]
        self.alpha = [0, 0]
        self.color = [(255,255,255), (255,255,255)]  
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
           
    def draw_rating(self, rating, index):
        """
        Renderiza avaliação com cor específica e fade-out.
        "Bad"=vermelho, "Good"=verde, "Perfect"=arco-íris.
        Retorna a cor usada.
        
        """
        if rating[index] != "":
            self.current_message[index] = rating[index]
            self.alpha[index] = 255
        
    def effect_text_rating(self): 
        """Anima cores RGB da cor padrão """   
        for i in range(3):
            self.def_col[i] += self.col_spd * self.col_dir[i]
            
            if self.def_col[i] >= 255:
                self.col_dir = 0
            elif self.def_col[i] <= 0:
                self.def_col[i] = 255
    def rainbow_effect(self):
        """ 
        Aplica efeito rainbow para os textos, ao percorrer a lista self.rainbow 
        e troca o index, fazendo o efeito rainbow

        """
        self.rainbow_change += self.rainbow_speed
        
        if self.rainbow_change > 1:
            self.rainbow_change = 0
            
            self.rainbow_index += 1
            
            if self.rainbow_index > 13:
                self.rainbow_index = 0        
        return self.rainbow[self.rainbow_index]
    
    def update(self, screen, combo, extra):
        """Chama todo frame para manter o fade-out ativo."""
        for index in range(len(self.current_message)):
            if self.alpha[index] > 0 and self.current_message[index] != "":
                if self.current_message[index] == "Bad":
                    self.color[index] = self.rainbow[1]
                elif self.current_message[index] == "Good":
                    self.color[index] = self.rainbow[5]
                elif self.current_message[index] == "Perfect":
                    self.color[index] = self.rainbow_effect()
                else:
                    self.color[index] = self.rainbow[-1]

                orig_surf = self.font.render(self.current_message[index], True, self.color[index])
                temp_surf = pygame.Surface(orig_surf.get_size(), pygame.SRCALPHA)
                temp_surf.set_alpha(self.alpha[index])
                temp_surf.blit(orig_surf, (0, 0))

                if self.mod == "Single Player":
                    screen.blit(temp_surf, (10, 300))
                else:
                    if index == 0:
                        screen.blit(temp_surf, (10, 300))
                    else:
                        screen.blit(temp_surf, (600, 300))
                
                if combo > 1:        
                    combo_text = self.font.render(f"Combo: {combo}", True, self.color[index])
                    screen.blit(combo_text, (10, 50))
                    
                    extra_text = self.font.render(f"+{extra}", True, self.color[index])
                    screen.blit(extra_text, (10, 90))

                self.alpha[index] = max(self.alpha[index] - 4, 0)
        return self.color[index]