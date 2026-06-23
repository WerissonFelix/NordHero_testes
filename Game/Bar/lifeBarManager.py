import pygame
import math


class LifeBarManager:
    """
    Gerencia a barra de vidas no modo Single Player.
    Exibe corações desenhados em Pygame puro.
    - Coração cheio  = vida ativa
    - Coração vazio  = vida perdida
    - Ao perder todas as vidas dispara on_game_over
    - No estado crítico (1 vida) o coração restante pulsa
    """

    def __init__(self, x, y, max_lives=3, heart_size=36, gap=12, on_game_over=None):
        self.x = x
        self.y = y
        self.max_lives = max_lives
        self.current_lives = max_lives
        self.heart_size = heart_size
        self.gap = gap
        self.on_game_over = on_game_over

        self.color_full = (220, 50, 50)
        self.color_empty = (90, 90, 90)
        self.color_critical = (255, 80, 80)

        self._pulse_tick = 0.0
        self._pulse_speed = 3.0

    def add_life(self):
        """  
        Adiciona um coração, caso o jogador tenha perdido algum.
        Adiciona se e somente se, ele já tinha perdido algum coração
        """
        
        if 0 < self.current_lives < 3:
            self.current_lives += 1
        else:
            pass
        
    def lose_life(self):
        """
        Remove uma vida.
        Retorna True se o jogador ainda está vivo.
        """
        
        if self.current_lives <= 0:
            return False

        self.current_lives -= 1

        if self.current_lives <= 0:
            if self.on_game_over:
                self.on_game_over()
            return False

        return True

    def is_alive(self):
        return self.current_lives > 0

    def is_critical(self):
        return self.current_lives == 1

    def reset(self):
        self.current_lives = self.max_lives
        self._pulse_tick = 0.0

    def handle_rating(self, rating: str):
        if rating == "Miss":
            return self.lose_life()
        elif rating == "Perfect":
            return self.add_life()
        return self.is_alive()

    def update(self, dt: float):
        """Avança o tick de pulsação. dt em segundos."""
        if self.is_critical():
            self._pulse_tick += dt * self._pulse_speed

    def draw(self, screen: pygame.Surface):
        step = self.heart_size + self.gap

        pulse_scale = 1.0
        if self.is_critical():
            pulse_scale = 1.0 + 0.12 * math.sin(self._pulse_tick * math.pi * 2)

        for i in range(self.max_lives):
            cx = self.x + i * step + self.heart_size // 2
            cy = self.y + self.heart_size // 2
            filled = i < self.current_lives

            if filled and self.is_critical():
                self._draw_heart(
                    screen,
                    cx, 
                    cy,
                    self.heart_size * pulse_scale,
                    self.color_critical,
                    filled=True
                )
            elif filled:
                self._draw_heart(
                    screen,
                    cx,
                    cy,
                    self.heart_size,
                    self.color_full,
                    filled=True
                )
            else:
                self._draw_heart(
                    screen, 
                    cx,
                    cy, 
                    self.heart_size,
                    self.color_empty,
                    filled=False
                )
                
    def _draw_heart(self, screen: pygame.Surface, cx: float, cy: float, size: float, color: tuple, filled: bool):
        """
        Desenha um coração usando dois círculos e um triângulo.
        cx, cy = centro visual do coração
        size = altura aproximada do coração em pixels
        """
        r = size * 0.28          
        tip_offset = size * 0.40 

        circle_y = cy - size * 0.10
        left_cx  = cx - r * 0.9
        right_cx = cx + r * 0.9
      
        tip_x = cx
        tip_y = cy + tip_offset
  
        triangle = [
            (left_cx - r, circle_y),   
            (right_cx + r, circle_y), 
            (tip_x, tip_y),
        ]

        if filled:
            pygame.draw.polygon(screen, color, triangle)
            
            pygame.draw.circle(screen, color,
                               (int(left_cx), int(circle_y)), int(r))
            pygame.draw.circle(screen, color,
                               (int(right_cx), int(circle_y)), int(r))
        else:
           
            pygame.draw.polygon(screen, color, triangle, 2)
            pygame.draw.circle(screen, color,
                               (int(left_cx), int(circle_y)), int(r), 2)
            pygame.draw.circle(screen, color,
                               (int(right_cx), int(circle_y)), int(r), 2)

    def get_total_width(self) -> int:
        return self.max_lives * self.heart_size + (self.max_lives - 1) * self.gap