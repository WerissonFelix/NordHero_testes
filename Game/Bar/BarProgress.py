import pygame


class BarProgressManager:
    """
    Gerencia a barra de progresso do modo Contra (futuramente para o modo juntos também).
    - Acumula acertos Perfect
    - Dispara um evento ao atingir o limite
    - Desenha a barra na tela
    """
    
    def __init__(self, x, y, width, height, threshold=10, event_callback=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.threshold = threshold
        self.progress = 0
        self.on_event = event_callback
        
        
        self.partner_bar = None
        self.on_both_full_callback = None

        self.fundo_color = (60, 60, 60)
        self.bar_color = (0, 200, 0)
        
    def add_perfect(self):
        """Adiciona um acerto Perfect e verifica se atingiu o limite."""
        
        if self.progress >= self.threshold:  
            
            if self.partner_bar and self.on_both_full_callback:
                
                if self.partner_bar.is_full():
                    self.reset()
                    self.partner_bar.reset()
                    
                    self.bar_color = (0, 200, 0)
                    self.partner_bar.bar_color = (0, 200, 0)
                    
                    self.on_both_full_callback()    
                else:
                    self.bar_color = (255, 215, 0)
                    
            else:    
                self.reset()
                
                if self.on_event:
                    self.on_event()
                
                return True
        else:
            self.progress +=1
        return False
    
    def add_bad_miss(self, index, rating):
        """  
        Adiciona um Miss ou Bad e verifica se atingiu o limite
        """
        if rating[index] in ["Bad", "Miss"]:
            self.progress += 1
            if self.progress >= self.threshold:
                self.reset()
                
                self.on_event()
            else:
                pass
        else:
            pass

    def draw(self, screen):
        """
        Primeiro desenha o fundo para depois desenhar a barra. 
        A barra tem tamanho variado, dependendo da quantidade 
        de notas perfeitas que o jogador acertou.
        """
        fundo = pygame.Rect(self.x, self.y, self.width, self.height)
        
        pygame.draw.rect(screen, self.fundo_color, fundo)
        
        atual_width = int((self.progress / self.threshold) * self.width)
        
        bar = pygame.Rect(self.x, self.y, atual_width, self.height)
        
        pygame.draw.rect(screen, self.bar_color, bar)
    
    def set_partner(self, other_bar, on_both_full_callback):
        """
        Define a barra parceira e o 
        callback para quando ambas estiverem cheias.
        """
        
        self.partner_bar = other_bar
        self.on_both_full_callback = on_both_full_callback

    def reset(self):
        """Reseta a barra para o início"""
        
        self.progress = 0
        
    def is_full(self):
        return self.progress >= self.threshold