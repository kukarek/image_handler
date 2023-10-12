import sql
from aiogram import types



def create_start_keyboard():

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    # Добавляем кнопки
    button1 = types.KeyboardButton("Франция")
    button2 = types.KeyboardButton("Испания")
    button3 = types.KeyboardButton("Румыния")

    keyboard.add(button1)
    keyboard.add(button2)
    keyboard.add(button3)

    return keyboard

def create_work_keyboard():

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    # Добавляем кнопки
    button1 = types.KeyboardButton("Получить фото")
    button2 = types.KeyboardButton("Главное меню")

    keyboard.add(button1)
    keyboard.add(button2)

    return keyboard

#обработка первого сообщения, юзера нет в бд, на любое сообщение будет запущена стартовая клава
def start_status_handler(user_id):
    
    sql.add_user(user_id=user_id) 
    text = ("Бим бим бам бам\n\n"+
            "Что будем лить?")

    return text, create_start_keyboard()

#обработка выбора страны
def choose_country(user_id, message_text):
    
    if message_text == "Франция":
        sql.set_status(user_id=user_id, status="FRANCE")
        text = "Переключаю крео на Францию!"

    elif message_text == "Испания":
        sql.set_status(user_id=user_id, status="SPAIN")
        text = "Переключаю крео на Испанию!"

    elif message_text == "Румыния":
        sql.set_status(user_id=user_id, status="ROMANIA")
        text = "Переключаю крео на Румынию!"

    else:
        return "Выберите на клавиатуре", None

    return text, create_work_keyboard() 

def work_status_handler(user_id, message_text):

    if message_text == "Главное меню":

        sql.set_status(user_id=user_id, status="start") 
        text = ("Бим бим бам бам\n\n"+
                "Что будем лить?")
        return text, create_start_keyboard()

    elif message_text == "Получить фото":
        #ничего не делаем
        return None, None
    
    else:
        text = "Чтобы изменить страну, перейдите в главное меню!"
        return text, None

#обработка входящего сообщения, возвращает текст ответа, клавиатуру, необходимость уведомить админа
def reply_message_handler(user_id, message_text):
                                        
    status = sql.get_status(user_id=user_id)[0]
        
    if status == "0":
        response, keyboard = start_status_handler(user_id=user_id)

    elif status == "start":
        response, keyboard = choose_country(user_id=user_id,message_text=message_text)

    else:
        response, keyboard = work_status_handler(user_id=user_id,message_text=message_text)

    return response, keyboard, status



