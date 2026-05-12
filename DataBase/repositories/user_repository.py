from DataBase.repositories.base_repository import BaseRepository
from models.user import User

class UserRepository(BaseRepository):
    
    def create(self, user: User):
        query =  """
        insert into user (name,email,password) 
        values(?, ?, ?)
        """
        self.execute(query, (user.name, user.email, user.password))
        
    def get_by_id(self, user_id):
        query = """
        select * from user 
        where id = ?
        """
        
        row = self.fetchone(query, (user_id,))
        
        if row is None: 
            return None
        
        return User(row[0], row[1], row[2], row[3])
    
           
    def get_by_email(self, email):
        query = """
        select * from user
        where email = ?
        """
        
        row = self.fetchone(query, (email,))
        
        if row is None:
            return None
        
        return User(row[0], row[1], row[2], row[3])
    
    
    def get_all(self):
        query = """
        select * from user
        """
        
        all_users = self.fetchall(query)
        
        rows = []
        
        for row in all_users:
            rows.append(User(
                row[0], row[1], row[2], row[3]
            ))
               
        return rows
    
    def update(self, user: User):
        query = """
        update user
        set name = ?, email = ?
        where id = ?
        """
        
        self.execute(query, (user.name, user.email, user.id))

    def delete(self, user_id):
        query = """
        delete from user 
        where id = ?
        """
        
        self.execute(query, (user_id,))
