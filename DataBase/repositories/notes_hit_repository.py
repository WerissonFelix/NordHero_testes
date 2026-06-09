from DataBase.repositories.base_repository import BaseRepository
from models.notes_hit import NotesHit


class NotesHitRepository(BaseRepository):
    """ 
    classe que manipula a tabela de notas acertadas, ou seja, a quantidade de miss, good e perfect.
    """
    def create(self, notes_hit: NotesHit):
        """
        cria um registro na tabela de notas acertadas, ou seja, a quantidade de miss, good e perfect.
        """
        query = """
        insert into notes_hit
        (user_id, chart_id, qtd_miss, qtd_bad, qtd_good, qtd_perfect)
        values (?, ?, ?, ?, ?, ?)
        """
        
        self.execute(query, (notes_hit.user_id, notes_hit.chart_id, notes_hit.qtd_miss, notes_hit.qtd_bad, notes_hit.qtd_good, notes_hit.qtd_perfect))
    
    def get_all(self):
        """ 
        busca todos os registros na tabela de notas acertadas, ou seja, a quantidade de miss, good e perfect.
        """
        query = """ 
        select * from notes_hit
        """
        
        rows = self.fetchall(query)
        
        if len(rows) == 0:
            return None
        
        notes_hit_list = []
        
        for row in rows:
            notes_hit_list.append(NotesHit(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        return notes_hit_list
    def get_by_id(self, notes_hit_id):
        """ 
        busca um registro na tabela de notas acertadas, ou seja, a quantidade de miss, good e perfect, pelo id.
        """
        query = """
        select * from notes_hit
        where id = ?
        """

        row = self.fetchone(query, (notes_hit_id,))
        
        if row is None:
            return None
        
        return NotesHit(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
    
    def get_by_user_chart_id(self, chart_id, user_id):
        """ 
        busca um registro na tabela de notas acertadas,
        ou seja, a quantidade de miss, good e perfect, pelo id do chart.
        """
        
        query = """ 
        select * from notes_hit
        where (chart_id = ? and user_id = ?)
        """
        
        row = self.fetchone(query, (chart_id, user_id))
        
        if row is None:
            return None
        
        return NotesHit(row[0], row[1], row[2], row[3], row[4], row[5], row[6])