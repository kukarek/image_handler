from aiogram import types
from misc.main_config import COUNTRY
from ..filters.bot_status import ON_OFF
from image_handler.config import handlers, Footage, Backgrounds, Preview
from image_handler.config import AVAILABLE_COUNTRYES



def create_start_keyboard(message: types.Message):

    keyboard = []
    
    for country in COUNTRY:
        
        keyboard.append([types.KeyboardButton(text=country)])

    return types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, selective=True)

def create_work_keyboard(message: types.Message):

    keyboard = []

    keyboard.append([types.KeyboardButton(text="Получить фото")])
    keyboard.append([types.KeyboardButton(text="Получить чистый фон")])
    keyboard.append([types.KeyboardButton(text="Главное меню")])
    
    return types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, selective=True)



def admin_panel_keyboard(message: types.Message):
    
    keyboard = []
    
    keyboard = [[types.KeyboardButton(text="Количество фонов"), types.KeyboardButton(text="Статистика пролива")],
                [types.KeyboardButton(text="Добавить администратора")],
                [types.KeyboardButton(text=("Запустить бота" if ON_OFF.status() == "Off" else "Остановить бота")), types.KeyboardButton(text="Конфиг")],
                [types.KeyboardButton(text="Количество пользователей")],
                [types.KeyboardButton(text="Рассылка")],
                [types.KeyboardButton(text="Редактировать страны")],
                [types.KeyboardButton(text="Главное меню")]
    ]

    return types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, selective=True)

def edit_country_keyboard(message: types.Message):

    keyboard = []

    for country in AVAILABLE_COUNTRYES():

        if country in COUNTRY:
            keyboard.append([types.KeyboardButton(text = f"Выключить {country}")])
        else:
            keyboard.append([types.KeyboardButton(text = f"Включить {country}")])

    keyboard.append([types.KeyboardButton(text="Завершить")])

    return  types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, selective=True)

def config_keyboard(message: types.Message):

    keyboard = [

        [types.KeyboardButton(text = ("Выключить футажи" if handlers.check(Footage()) else "Включить футажи"))],
        [types.KeyboardButton(text = ("Выключить фон" if handlers.check(Backgrounds()) else "Включить фон"))],
        [types.KeyboardButton(text = ("Выключить превью" if handlers.check(Preview()) else "Включить превью"))],
        [types.KeyboardButton(text = "Завершить")]

    ]

    return types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, selective=True)
