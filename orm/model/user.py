from orm.database import sql


class User:
    

    def __init__(self, id):
        self.id = id

    def new(self):
        
        result = sql.run(f'''
        SELECT EXISTS (
            SELECT 1
            FROM users
            WHERE user_id = ?
            LIMIT 1
        );
        ''', (self.id,))[0][0]

        if result != 1:
            
            sql.run(f'''
            INSERT INTO users (user_id, status)
            VALUES (?, ?);
            ''', (self.id, "start"))
            
        else:
            
            sql.run(f'''
            UPDATE users
            SET status = ?
            WHERE user_id = ?;
            ''', ("start", self.id))  

    def set_status(self, status):

        sql.run(f'''
        UPDATE users
        SET status = ?
        WHERE user_id = ?;
        ''', (status, self.id))

    def set_admin_status(self, status):
    
        sql.run(f'''
        UPDATE users
        SET admin_status = ?
        WHERE user_id = ?;
        ''', (status, self.id))

    def set_country(self, country):
    
        sql.run(f'''
        UPDATE users
        SET country = ?
        WHERE user_id = ?;
        ''', (country, self.id))
 
    def get_status(self):

        # Запрос для проверки наличия записи с заданным user_id
        result = sql.run(f'''
        SELECT EXISTS (
            SELECT 1
            FROM users
            WHERE user_id = ?
            LIMIT 1
        );
        ''', (self.id,))[0][0]

        if result == 1:

            return sql.run( f'''
            SELECT status
            FROM users
            WHERE user_id = ?;
            ''', (self.id,))[0][0]
        
        else:
            return "0"
        
    def get_admin_status(self):

        # Запрос для проверки наличия записи с заданным user_id
        result = sql.run(f'''
        SELECT EXISTS (
            SELECT 1
            FROM users
            WHERE user_id = ?
            LIMIT 1
        );
        ''', (self.id,))[0][0]
        
        if result == 1:
            
            return sql.run(f'''
            SELECT admin_status
            FROM users
            WHERE user_id = ?;
            ''', (self.id,))[0][0]
        
        else:
            return "0"
        
    def get_country(self):

        result = sql.run(f'''
        SELECT EXISTS (
            SELECT 1
            FROM users
            WHERE user_id = ?
            LIMIT 1
        );
        ''', (self.id,))[0][0]
        
        if result == 1:
            
            return sql.run(f'''
            SELECT country
            FROM users
            WHERE user_id = ?;
            ''', (self.id,))[0][0]
            
        else:
            return "0"

    def get_all_users(self):

        return sql.run(f'''
        SELECT user_id
        FROM users;
        ''')[0][0]
    
    def get_user_info(self):

        result = sql.run(f'''
        SELECT EXISTS (
            SELECT 1
            FROM users
            WHERE user_id = ?
            LIMIT 1
        );
        ''', (self.id,))[0][0]
        
        if result == 1:

            return sql.run(f'''
            SELECT *
            FROM users
            WHERE user_id = ?;
            ''', (self.id,))[0][0]
        
        else:
            return "0"


