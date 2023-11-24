from aiogram import types
from misc.main_config import COUNTRY, AVAILABLE_COUNTRYES, ADMINS
from ..filters.bot_status import ON_OFF
from image_handler.config import handlers, Footage, Backgrounds, Preview



def create_start_keyboard(message: types.Message):

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    
    for country in COUNTRY:
        keyboard.add(types.KeyboardButton(country))

    return keyboard

def create_work_keyboard(message: types.Message):

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    keyboard.add(types.KeyboardButton("Получить фото"))
    for admin in ADMINS:
        if admin == message.from_id:
            keyboard.add(types.KeyboardButton("Получить видео"))
    keyboard.add(types.KeyboardButton("Главное меню"))

    return keyboard

def admin_panel_keyboard(message: types.Message):
    
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, selective=True)
    
    button1 = types.KeyboardButton("Количество фонов")
    button2 = types.KeyboardButton("Статистика пролива")
    button3 = types.KeyboardButton("Добавить администратора")

    if ON_OFF.status() == "Off":
        button4 = types.KeyboardButton("Запустить бота")
    else:
        button4 = types.KeyboardButton("Остановить бота")

    button5 = types.KeyboardButton("Конфиг")

    button6 = types.KeyboardButton("Количество пользователей")
    button7 = types.KeyboardButton("Рассылка")
    button8 = types.KeyboardButton("Редактировать страны")
    button9 = types.KeyboardButton("Главное меню")


    keyboard.add(button1, button2)
    keyboard.add(button3)
    keyboard.add(button4, button5)
    keyboard.add(button6)
    keyboard.add(button7)
    keyboard.add(button8)
    keyboard.add(button9)

    return keyboard

def edit_country_keyboard(message: types.Message):

    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, selective=True)

    for country in AVAILABLE_COUNTRYES():

        if country in COUNTRY:
            keyboard.add(types.KeyboardButton(f"Выключить {country}"))
        else:
            keyboard.add(types.KeyboardButton(f"Включить {country}"))


    keyboard.add(types.KeyboardButton("Завершить"))

    return keyboard

def config_keyboard(message: types.Message):

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, selective=True)

    if handlers.check(Footage()):
        button1 = types.KeyboardButton("Выключить футажи")
    else:
        button1 = types.KeyboardButton("Включить футажи")

    if handlers.check(Backgrounds()):
        button2 = types.KeyboardButton("Выключить фон")
    else:
        button2 = types.KeyboardButton("Включить фон")

    if handlers.check(Preview()):
        button3 = types.KeyboardButton("Выключить превью")
    else:
        button3 = types.KeyboardButton("Включить превью")

    keyboard.add(button1, button2, button3)
    keyboard.add(types.KeyboardButton("Завершить"))

    return keyboard
