
class GameEvents:
    """
    Centraliza todos os eventos que podem ocorrer quando uma barra de progresso
    é ativada.
    """
    
    def penalty_loss_points(opponent_index, score, rating):
        """
        Aplica penalidade de -500 pontos ao oponente.
        """
        
        loss = 500
        score[opponent_index] = max(0, score[opponent_index] - loss)
        
        rating[opponent_index] = "Penalty!"