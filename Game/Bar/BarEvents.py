from Game.Text.TextManager import TextManager
import pygame
class BarEvents:
    """
    Centraliza todos os eventos que podem ocorrer quando uma barra de progresso
    é ativada.
    """
    def __init__(self, screen, mod, text_manager: TextManager):
        self.mod = mod
        self.screen = screen
        self.txtManager = text_manager
        self.font = pygame.font.Font(None, 36)
        
    
    def penalty_loss_points(self, opponent_index, score, rating):
        """
        Aplica penalidade de -500 pontos ao oponente.
        """
        loss = 500
        score[opponent_index] = max(0, score[opponent_index] - loss)
        
        rating[opponent_index] = "Penalty!"
        
        if opponent_index == 0:
            posi1, posi2 = (200, 10), (900, 10)
            msg1 = "-500 pontos"
            msg2 = "+500 pontos"
            col1, col2 = (255,0,0), (0,255,0)
        else:
            posi1, posi2 = (900, 10), (200, 10)
            msg1 = "-500 pontos"
            msg2 = "+500 pontos"
            col1, col2 = (255,0,0), (0,255,0)
       
        self.txtManager.add_notification(msg1, posi1, col1, duration_frames=60)
        self.txtManager.add_notification(msg2, posi2, col2, duration_frames=60)