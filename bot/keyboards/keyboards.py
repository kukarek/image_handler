from aiogram import types
from misc.main_config import ON_OFF
from image_handler.config import handlers, Footage, Backgrounds, Preview



def create_start_keyboard():

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    
    button1 = types.KeyboardButton("FRANCE")
    button2 = types.KeyboardButton("SPAIN")
    button3 = types.KeyboardButton("ROMANIA")

    keyboard.add(button1)
    keyboard.add(button2)
    keyboard.add(button3)

    return keyboard

def create_work_keyboard():

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    
    button1 = types.KeyboardButton("Получить фото")
    button2 = types.KeyboardButton("Главное меню")

    keyboard.add(button1)
    keyboard.add(button2)

    return keyboard

def admin_panel_keyboard():

    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, selective=True)
    
    button1 = types.KeyboardButton("Количество фонов")
    button2 = types.KeyboardButton("Статистика пролива")
    button3 = types.KeyboardButton("Добавить администратора")

    if ON_OFF == "On":
        button4 = types.KeyboardButton("Остановить бота")
    else:
        button4 = types.KeyboardButton("Запустить бота")

    button6 = types.KeyboardButton("Конфиг")

    if handlers.check(Footage()):
        button7 = types.KeyboardButton("Выключить футажи")
    else:
        button7 = types.KeyboardButton("Включить футажи")

    if handlers.check(Backgrounds()):
        button8 = types.KeyboardButton("Выключить фон")
    else:
        button8 = types.KeyboardButton("Включить фон")

    if handlers.check(Preview()):
        button9 = types.KeyboardButton("Выключить превью")
    else:
        button9 = types.KeyboardButton("Включить превью")

    button10 = types.KeyboardButton("Количество пользователей")
    button11 = types.KeyboardButton("Рассылка")
    button12 = types.KeyboardButton("Главное меню")


    keyboard.add(button1, button2)
    keyboard.add(button3)
    keyboard.add(button4, button6)
    keyboard.add(button7)
    keyboard.add(button8)
    keyboard.add(button9)
    keyboard.add(button10)
    keyboard.add(button11)
    keyboard.add(button12)

    return keyboard