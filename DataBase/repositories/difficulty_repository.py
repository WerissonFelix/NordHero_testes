from DataBase.repositories.base_repository import BaseRepository
from models.difficulty import Difficulty

class DifficultyRepository(BaseRepository):
    
    def create_difficulty(self, difficulty: Difficulty):
        query = """
        insert into difficulties (name)
        values (?)
        """
        
        self.execute(query, (difficulty.name,))
    
    def get_by_name(self, name: str):
        query = """
        select * from difficulties
        where name = ?
        """
        
        row = self.fetchone(query, (name,))
        
        if row is None:
            return None
        
        return Difficulty(row[0], row[1])
    def get_all(self):
        query = """
        select * from difficulties
        """
        
        rows = self.fetchall(query)
        
        if len(rows) == 0:
            return None
        else:
            all_difficulties = [Difficulty(row[0], row[1]) for row in rows]
        return all_difficulties


"""   
difficultyManeger = DifficultyRepository()


easy = Difficulty(None, "Easy")
normal = Difficulty(None, "Normal")
hard = Difficulty(None, "Hard")

difficultyManeger.create_difficulty(easy)
difficultyManeger.create_difficulty(normal)
difficultyManeger.create_difficulty(hard)

"""