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
        
        self.fundo_color = (60, 60, 60)
        self.bar_color = (0, 200, 0)
        
    def add_perfect(self):
        """Adiciona um acerto Perfect e verifica se atingiu o limite."""
        
        self.progress +=1
        
        if self.progress >= self.threshold:
            self.progress = 0
            
            self.reset()
            if self.on_event:
                self.on_event()
            
            return True
        return False

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
    
    def reset(self):
        """Reseta a barra para o início"""
        
        self.progress = 0
         
        