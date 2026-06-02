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
        (chart_id, qtd_miss, qtd_bad,qtd_good, qtd_perfect)
        values (?, ?, ?, ?, ?)
        """
        
        self.execute(query, (notes_hit.chart_id, notes_hit.qtd_miss, notes_hit.qtd_bad, notes_hit.qtd_good, notes_hit.qtd_perfect))
        
    def get_by_id(self, notes_hit_id):
        """ 
        busca um registro na tabela de notas acertadas, ou seja, a quantidade de miss, good e perfect, pelo id.
        """
        query = """"
        select * from notes_hit
        where id = ?
        """

        row = self.fetchone(query, (notes_hit_id,))
        
        if row is None:
            return None
        
        return NotesHit(row[0], row[1], row[2], row[3], row[4], row[5])
    
    def get_by_chart_id(self, chart_id):
        """ 
        busca um registro na tabela de notas acertadas,
        ou seja, a quantidade de miss, good e perfect, pelo id do chart.
        """
        
        query = """ 
        select * from notes_hit
        where chart_id = ?
        """
        
        row = self.fetchone(query, (chart_id, ))
        
        if row is None:
            return None
        
        return NotesHit(row[0], row[1], row[2], row[3], row[4], row[5])