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
        self.notifications = []   # cada item: {"text": str, "pos": (x,y), "color": tuple, "life": int, "alpha": int}

    def add_notification(self, text, pos, color, duration_frames=30):
        """Adiciona uma mensagem que desaparece após alguns frames."""
        self.notifications.append({
            "text": text,
            "pos": pos,
            "color": color,
            "life": duration_frames,
            "alpha": 255
        })

    def update_notifications(self, screen):
        """Desenha todas as notificações ativas e reduz seu tempo de vida."""
        to_remove = []
        for notif in self.notifications:
            alpha = int(255 * (notif["life"] / 30)) 
            surf = self.font.render(notif["text"], True, notif["color"])
            surf.set_alpha(alpha)
            screen.blit(surf, notif["pos"])
            notif["life"] -= 1
            if notif["life"] <= 0:
                to_remove.append(notif)
        for n in to_remove:
            self.notifications.remove(n)

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
    
    def update(self, screen, combo=None, extra=None):
        """Chama todo frame para manter o fade-out ativo."""
        for index in range(len(self.current_message)):
            if self.alpha[index] > 0 and self.current_message[index] != "":
                if self.current_message[index] == "Bad":
                    self.color[index] = self.rainbow[1]
                elif self.current_message[index] == "Good":
                    self.color[index] = self.rainbow[5]
                elif self.current_message[index] == "Perfect":
                    self.color[index] = self.rainbow_effect()
                elif self.current_message[index] in ["Trap!", "Penalty!"]:
                    self.color[index] = self.rainbow[2]
                    if index == 0:
                        posi1, posi2 = (50, 10), (750, 10)
                        msg1 = "-300 pontos" if self.current_message[index] == "Trap!" else "-500 pontos"
                        msg2 = "+300 pontos" if self.current_message[index] == "Trap!" else "+500 pontos"
                    else:
                        posi1, posi2 = (750, 10), (50, 10)
                        msg1 = "-300 pontos" if self.current_message[index] == "Trap!" else "-500 pontos"
                        msg2 = "+300 pontos" if self.current_message[index] == "Trap!" else "+500 pontos"
                    
                    surf1 = self.font.render(msg1, True, self.rainbow[1])
                    surf2 = self.font.render(msg2, True, self.rainbow[5])
                    screen.blit(surf1, posi1)
                    screen.blit(surf2, posi2)
                    return self.color[index]
                else:
                    self.color[index] = self.rainbow[-1]

                orig_surf = self.font.render(self.current_message[index], True, self.color[index])
                temp_surf = pygame.Surface(orig_surf.get_size(), pygame.SRCALPHA)
                temp_surf.set_alpha(self.alpha[index])
                temp_surf.blit(orig_surf, (0, 0))

                if self.mod == "Single Player":
                    screen.blit(temp_surf, (10, 300))
                else:
                    posi = (10, 300) if index == 0 else (700, 300)
                    screen.blit(temp_surf, posi)

                if combo[index] > 1:        
                    combo_text = self.font.render(f"Combo: {combo}", True, self.color[index])
                    extra_text = self.font.render(f"+{extra}", True, self.color[index])
                    if index == 0:
                        screen.blit(combo_text, (10, 50))
                        screen.blit(extra_text, (10, 90))
                    else:
                        screen.blit(combo_text, (700, 50))
                        screen.blit(extra_text, (700, 90))   
                self.alpha[index] = max(self.alpha[index] - 4, 0)
        self.update_notifications(screen)
        return self.color[index]