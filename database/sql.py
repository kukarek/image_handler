import sqlite3
from misc.main_config import DB

#sql запросы
def set_status(user_id, status):
   
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    # Запрос для обновления статуса по user_id
    update_status_query = f'''
    UPDATE users
    SET status = ?
    WHERE user_id = ?;
    '''
    # Выполнение запроса с передачей параметров new_status и user_id
    cursor.execute(update_status_query, (status, user_id))
    # Сохранение изменений и закрытие подключения к базе данных
                
    conn.commit()
    conn.close()

def set_country(user_id, country):
   
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    update_status_query = f'''
    UPDATE users
    SET country = ?
    WHERE user_id = ?;
    '''

    cursor.execute(update_status_query, (country, user_id))
                
    conn.commit()
    conn.close()


def add_user(user_id):
    
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    # Запрос для проверки наличия записи с заданным user_id
    check_user_query = f'''
    SELECT EXISTS (
        SELECT 1
        FROM users
        WHERE user_id = ?
        LIMIT 1
    );
    '''
    # Выполнение запроса с передачей параметра user_id
    cursor.execute(check_user_query, (user_id,))
    result = cursor.fetchone()[0]

    if result != 1:
        query = f'''
        INSERT INTO users (user_id, status)
        VALUES (?, ?);
        '''
        cursor.execute(query, (user_id, "start"))
        
    else:
        query = f'''
        UPDATE users
        SET status = ?
        WHERE user_id = ?;
        '''
        cursor.execute(query, ("start", user_id))   

                
    conn.commit()
    conn.close()


def get_status(user_id):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    # Запрос для проверки наличия записи с заданным user_id
    check_user_query = f'''
    SELECT EXISTS (
        SELECT 1
        FROM users
        WHERE user_id = ?
        LIMIT 1
    );
    '''
    # Выполнение запроса с передачей параметра user_id
    cursor.execute(check_user_query, (user_id,))
    result = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    
    if result == 1:
       conn = sqlite3.connect(DB)
       cursor = conn.cursor()
       # Запрос для получения статуса по user_id
       get_status_query = f'''
       SELECT status
       FROM users
       WHERE user_id = ?;
       '''
       # Выполнение запроса с передачей параметра user_id
       cursor.execute(get_status_query, (user_id,))
       status = cursor.fetchone()

       conn.commit()
       conn.close()

       return status
    
    else:
       return "0"
    
def get_country(user_id):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    # Запрос для проверки наличия записи с заданным user_id
    check_user_query = f'''
    SELECT EXISTS (
        SELECT 1
        FROM users
        WHERE user_id = ?
        LIMIT 1
    );
    '''
    # Выполнение запроса с передачей параметра user_id
    cursor.execute(check_user_query, (user_id,))
    result = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    
    if result == 1:
       conn = sqlite3.connect(DB)
       cursor = conn.cursor()
       # Запрос для получения статуса по user_id
       query = f'''
       SELECT country
       FROM users
       WHERE user_id = ?;
       '''
       # Выполнение запроса с передачей параметра user_id
       cursor.execute(query, (user_id,))
       country = cursor.fetchone()

       conn.commit()
       conn.close()

       return country
    
    else:
       return "0"

def get_all_users():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    get_status_query = f'''
       SELECT user_id
       FROM users;
       '''
    # Выполнение запроса с передачей параметра user_id
    cursor.execute(get_status_query)
    users_id = cursor.fetchall()

    conn.commit()
    conn.close()

    return users_id

def get_user_info(user_id):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    # Запрос для проверки наличия записи с заданным user_id
    check_user_query = f'''
    SELECT EXISTS (
        SELECT 1
        FROM users
        WHERE user_id = ?
        LIMIT 1
    );
    '''
    # Выполнение запроса с передачей параметра user_id
    cursor.execute(check_user_query, (user_id,))
    result = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    
    if result == 1:
       conn = sqlite3.connect(DB)
       cursor = conn.cursor()
       # Запрос для получения статуса по user_id
       get_status_query = f'''
       SELECT *
       FROM users
       WHERE user_id = ?;
       '''
       # Выполнение запроса с передачей параметра user_id
       cursor.execute(get_status_query, (user_id,))
       info = cursor.fetchone()

       conn.commit()
       conn.close()

       return info
    
    else:
       return "0"

#созданию соединения (не используется в коде)
def create_connection():
    
    connection = sqlite3.connect(DB)
    cursor = connection.cursor()

    # Создаем таблицу для хранения подписок пользователей, если она не существует
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (user_id INTEGER PRIMARY KEY, status TEXT, country TEXT)''')

    connection.commit()
    connection.close()
