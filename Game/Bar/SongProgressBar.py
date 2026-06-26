import pygame

class SongProgressBar:
    """
    Barra de progresso da música durante a gameplay.
    Aumenta da esquerda pra direita conforme o tempo avança.
    """
    def __init__(self, x, y, width, height, duration_ms, bar_color=(138, 92, 246), bg_color=(60, 60, 60),
        show_time=True, font=None):
        
        self.x = x
        self.y = y
        
        self.width = width
        self.height = height
        
        self.duration_ms = duration_ms
        self.bar_color = bar_color
        self.bg_color = bg_color
        
        self.show_time = show_time
        self.font = font or pygame.font.Font(None, 24)
        self.current_ms = 0

    def update(self, current_ms):
        """
        Atualiza o progresso. 
        Recebe o tempo atual em ms (mixer.music.get_pos()).
        """
        
        self.current_ms = max(0, min(current_ms, self.duration_ms))

    def draw(self, screen):
        progress = self.current_ms / self.duration_ms if self.duration_ms > 0 else 0

        bg_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.bg_color, bg_rect, border_radius=self.height // 2)

        fill_w = int(progress * self.width)
        if fill_w > 0:
            fill_rect = pygame.Rect(self.x, self.y, fill_w, self.height)
            pygame.draw.rect(screen, self.bar_color, fill_rect, border_radius=self.height // 2)

        if self.show_time:
            def fmt(ms):
                s = ms // 1000
                
                return f"{s // 60}:{s % 60:02d}"

            cur = self.font.render(fmt(self.current_ms), True, (200, 200, 200))
            tot = self.font.render(fmt(self.duration_ms), True, (150, 150, 150))
            
            screen.blit(cur, (self.x, self.y + self.height + 4))
            screen.blit(tot, (self.x + self.width - tot.get_width(), self.y + self.height + 4))