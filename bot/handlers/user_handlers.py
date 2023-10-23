from database import sql
from aiogram.types import Message
from ..keyboards.keyboards import *
import logging
from image_handler import image_handler 
from io import BytesIO
from aiogram.types import InputMediaPhoto
from misc.main_config import THREADS, COUNTRY



async def start_status_handler(message: Message):
    
    sql.add_user(message.from_id) 
    text = ("Бим бим бам бам\n\n"+
            "Что будем лить?")

    await message.answer(text=text, reply_markup=create_start_keyboard())

#обработка выбора страны
async def choose_country(message: Message):
    
    if message.text in COUNTRY:
        sql.set_status(message.from_id, "work")
        sql.set_country(message.from_id, message.text)

        text = f"Переключаю крео на {message.text}!"
        await message.answer(text=text, reply_markup=create_work_keyboard()) 
    else:
        await message.answer(text="Выберите на клавиатуре")
    

async def work_status_handler(message: Message):

    country = sql.get_country(message.from_id)[0]


    COUNTRY[country]["strait"] += 1

    images = image_handler.conversion(country=country)

    THREADS.append("thread")
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

    await message.answer_media_group("Большая нагрузка на бота, попробуйте позже...")

async def bot_disable(message: Message):

    await message.answer_media_group("Бот временно остановлен администратором")

        