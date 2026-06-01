from DataBase.repositories.base_repository import BaseRepository
from models.notes_hit import NotesHit


class NotesHitRepository(BaseRepository):
    
    def create(self, notes_hit: NotesHit):
        query = """"
        insert into notes_hit
        (qtd_miss, qtd_good, qtd_perfect)
        values (?, ?, ?)
        """
        
        self.execute(query, (notes_hit.qtd_miss, notes_hit.qtd_good, notes_hit.qtd_perfect))
        
    def get_by_id(self, notes_hit_id):
        query = """"
        select * from notes_hit
        where id = ?
        """

        row = self.fetchone(query, (notes_hit_id,))
        
        if row is None:
            return None
        
        return NotesHit(row[0], row[1], row[2], row[3])