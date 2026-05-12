from DataBase.repositories.base_repository import BaseRepository
from models.difficulty import Difficulty

class DifficultyRepository(BaseRepository):
    
    def create_difficulty(self,difficulty: Difficulty):
        query = """
        insert into difficulties (name)
        values (?)
        """
        
        self.execute(query,(difficulty.name,))
    
    def get_by_name(self, name):
        query = """
        select * from difficulties
        where name = ?
        """
        
        row = self.fetchone(query, (name,))
        
        if row is None:
            return None
        
        return Difficulty(row[0], row[1])