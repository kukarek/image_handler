import sqlite3
from misc.main_config import DB
from log.logger import log


def run(query, values = ()) -> str:

    try:
        
        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        
        cursor.execute(query, values)

        result = cursor.fetchall()

        connection.commit()
        connection.close()

        return result
    
    except Exception as e:

        log.error(e)
        print(e)

#созданию соединения (создает бд)
def create_db():
    
    
    connection = sqlite3.connect(DB)
    cursor = connection.cursor()

    # Создаем таблицу для хранения подписок пользователей, если она не существует
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (user_id INTEGER PRIMARY KEY, status TEXT, country TEXT, admin_status TEXT)''')

    connection.commit()
    connection.close()