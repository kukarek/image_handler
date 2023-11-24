from database import sql
from aiogram import Dispatcher
from aiogram.types import Message
from ..keyboards.keyboards import *
import logging
from image_handler import image_handler 
from io import BytesIO
from aiogram.types import InputMediaPhoto
from misc.main_config import COUNTRY
from ..filters.bot_status import THREADS
from aiogram.dispatcher.filters import Text
from ..filters.admin_status import *
from ..filters.user_status import *
from ..filters.bot_status import *



async def start_status_handler(message: Message):
    
    sql.add_user(message.from_id) 
    text = ("Бим бим бам бам\n\n"+
            "Что будем лить?")

    await message.answer(text=text, reply_markup=create_start_keyboard(message))

#обработка выбора страны
async def choose_country(message: Message):
    
    if message.text in COUNTRY:
        sql.set_status(message.from_id, "work")
        sql.set_country(message.from_id, message.text)

        text = f"Переключаю крео на {message.text}!"
        await message.answer(text=text, reply_markup=create_work_keyboard(message)) 
    else:
        await message.answer(text="Выберите на клавиатуре")
    

async def work_status_handler(message: Message):

    country = sql.get_country(message.from_id)[0]


    COUNTRY[country]["strait"] += 1

    images = image_handler.conversion(country=country)

    THREADS.add()
    #конвертация из Image в InputMediaPhoto для тг
    media = []
    for image in images:

        image_stream = BytesIO()
        image.save(image_stream, format='JPEG')
        image_stream.seek(0)
        media.append(InputMediaPhoto(media=image_stream))

    THREADS.pop()

    await message.answer_media_group(media = media)

async def choose_in_keyboard(message: Message):

    await message.answer("Выберите на клавиатуре..")

async def huge_pressure(message: Message):

    await message.answer("Большая нагрузка на бота, попробуйте позже...")

async def bot_disable(message: Message):

    await message.answer("Бот временно остановлен администратором")

def register_user_handlers(dp: Dispatcher):

    dp.register_message_handler(bot_disable, isUser() & botDisable())
    dp.register_message_handler(start_status_handler, isUser() & botEnable() | isAdmin(), commands=['start'])
    dp.register_message_handler(start_status_handler, isUser() & botEnable() & user_isWork() | isAdmin() & user_isWork(), Text(equals="Главное меню"))
    dp.register_message_handler(start_status_handler, isUser() & botEnable() & user_isNone() | isAdmin() & user_isNone())
    dp.register_message_handler(choose_country, isUser() & botEnable() & user_isStart() | isAdmin() & user_isStart())
    dp.register_message_handler(huge_pressure, isUser() & botEnable() & user_isWork() & Huge_Pressure() | isAdmin() & user_isWork() & Huge_Pressure())
    dp.register_message_handler(start_status_handler, isUser() & botEnable() & user_isWork() & Incorrect_Country() | isAdmin() & user_isWork(), Incorrect_Country())
    dp.register_message_handler(work_status_handler, isUser() & botEnable() & user_isWork() | isAdmin() & user_isWork(), Text(equals="Получить фото"))
    dp.register_message_handler(choose_in_keyboard, isUser() & botEnable() & user_isWork() | isAdmin() & user_isWork())

