from DataBase.repositories.base_repository import BaseRepository
from models.score import Score

class ScoreRepository(BaseRepository):
    
    def create(self, score: Score):
        query = """
        insert into scores 
        (user_id, chart_id, score, accuracy, rank)
        values (?, ?, ?, ?, ?)
        """
        
        self.execute(query, (score.user_id, score.chart_id, score.score, score.accuracy, score.rank))
    
    def delete(self, score_id):
        query = """ 
        delete from scores 
        where id = ?
        """
        
        self.execute(query, (score_id, ))    
    """ 
    ===========================================================
            FUNÇÕES RELACIONADOS PARA UM USER (UM JOGADOR)
    ===========================================================
    """
    def get_all_by_user_id(self, user_id):
        """ 
        Manda a query de busca para manipular todos os scores de todas as músicas/charts.
        Muito importante para fazer um histórico pessoal, ou até mesmo um gráfico de progressão
        de habilidades. (possível feature??????)
        
        Retorna uma lista, onde cada elemento é o tipo Score, da class models.
        
        """
        query = """
        select * from scores
        where user_id = ?
        """
        
        rows = self.fetchall(query, (user_id, ))
        
        all_scores = []
        
        if rows is None:
            return None
        
        for row in rows:
            all_scores.append(Score(row[0],row[1], row[2], row[3], row[4], row[5]))
        return all_scores

    def get_by_user_chart_id(self, user_id, chart_id):
        query = """
        select * from scores
        where (user_id = ? and song_id = ?)
        """
        
        rows = self.fetchall(query, (user_id, chart_id))
        
        if rows is None:
            return None
        
        all_scores = []
        
        for row in rows:
            all_scores.append(Score(row[0],row[1], row[2], row[3], row[4], row[5]))
        return all_scores
    
    def get_by_user_difficulty(self, user_id, difficulty_id):
        query = """  
        select scores.*
        from scores
        inner join song_charts ON scores.chart_id = song_charts.id
        
        where (scores.user_id = ? and song_charts.difficulty_id = ?)
        """
        
        rows = self.fetchall(query, (user_id, difficulty_id))
        
        if rows is None:
            return None
        
        all_scores = []
        
        for row in rows:
            all_scores.append(Score(row[0],row[1], row[2], row[3], row[4], row[5]))
        return all_scores
    
    def get_best_by_user_and_chart(self, user_id, chart_id):
        """ 
        Retorna o melhor score do jogador naquele chart especifico 
        """
        
        query = """
        select * from scores
        
        where (user_id = ? and chart_id = ?)
        
        order by score DESC
        limit 1
        """
        
        row = self.fetchone(query, (user_id, chart_id))
        
        if row is None:
            return None
        
        return Score(row[0],row[1], row[2], row[3], row[4], row[5])
        