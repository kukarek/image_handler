import sqlite3
from config import DB

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

def add_user(user_id):
    
    #подключение в базе данных 
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    #запрос на добавление нового юзера со статусом по умолчанию - start 
    add_user_query = f'''
    INSERT INTO users (user_id, status)
    VALUES (?, ?);
    '''
    #Выполнение запроса с передачей параметров user_id и status
    cursor.execute(add_user_query, (user_id, "start"))
    # Сохранение изменений и закрытие подключения к базе данных
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
                      (user_id INTEGER PRIMARY KEY, status TEXT)''')

    connection.commit()
    connection.close()
