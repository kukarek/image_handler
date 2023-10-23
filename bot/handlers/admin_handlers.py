import logging
from aiogram import types
from aiogram.types import Message
import time
from database import sql
from ..main import bot
from ..keyboards.keyboards import admin_panel_keyboard
from image_handler.config import handlers
from image_handler.handlers.preview import Preview
from image_handler.handlers.backgrounds import Backgrounds
from image_handler.handlers.footage import Footage
from misc.main_config import ADMINS, BACKGROUNDS_LIST, ON_OFF, COUNTRY


async def count(message: Message):
    
    with open(BACKGROUNDS_LIST, 'r') as file:
        # Прочитайте строки из файла и создайте массив ссылок
        links = [line.strip() for line in file]

    await message.answer(text=len(links))

async def stats(message: Message):
    
    text = "Пролив:\n"

    for country in COUNTRY:
        if COUNTRY[country]["strait"] != 0:
            text += f"{country}: {COUNTRY[country]['strait']}\n"
    
    await message.answer(text)

async def add_backgrounds(message: types.Message):
    
    try:
        
        time.sleep(10)
        # Скачиваем документ
        file_path = await bot.get_file(message.document.file_id)
        document = await bot.download_file(file_path.file_path)

        # Извлекаем текст из загруженного документа
        document_bytes = document.read()
        new_backgrounds = document_bytes.decode("utf-8")      
        new_backgrounds = new_backgrounds.replace("\r", "") 

        with open(BACKGROUNDS_LIST, "a") as file:
            # Добавляем новый текст с новой строкой
            file.write("\n"+ new_backgrounds)   

        await message.answer(text="Фоны успешно добавлены!")

    except:
        await message.answer("Произошла ошибка")

async def help(message: Message):

    await message.answer(f"{message.chat.first_name}, добро пожаловать в админ панель!", reply_markup = admin_panel_keyboard())            

async def add_admin(message: Message):
    #добавление администратора
    #если команда указана в начале
    if "add" in message.text.split(" ", 1)[0]:
        admin_id = int(message.text.split(" ")[2])
        ADMINS.append(admin_id)
        await message.answer(f"Добавлен администратор с id: {admin_id}")

async def bot_stop(message: Message):
    global ON_OFF
    #остановка бота
    if ON_OFF == "On":
        ON_OFF = "Off"
        await message.answer("Остановка бота", reply_markup=admin_panel_keyboard())
    else:
        await message.answer("Бот уже остановлен", reply_markup=admin_panel_keyboard())

async def bot_start(message: Message):
    global ON_OFF
    #запуск бота
    if ON_OFF == "Off":
        ON_OFF = "On"
        await message.answer("Запуск бота", reply_markup=admin_panel_keyboard())
    else:
        await message.answer("Бот уже запущен", reply_markup=admin_panel_keyboard())

async def bot_status(message: Message):

    await message.answer(ON_OFF)

async def config(message: Message):

    config = "Текущая настройка:\n"
    for handler in handlers.get_handlers():
        config += f"{handler.key}\n"

    await message.answer(config)

async def footage_on(message: Message):
        
    handlers.append(Footage())

    await message.answer("Футажи включены!", reply_markup=admin_panel_keyboard())
    
async def footage_off(message: Message):

    handlers.remove(Footage())
        
    await message.answer("Футажи выключены!", reply_markup=admin_panel_keyboard())

async def background_on(message: Message):
        
    handlers.append(Backgrounds())

    await message.answer("Фоны включены!", reply_markup=admin_panel_keyboard())
    
async def background_off(message: Message):

    handlers.remove(Backgrounds())
        
    await message.answer("Фоны выключены!", reply_markup=admin_panel_keyboard())

async def preview_on(message: Message):
        
    handlers.append(Preview())

    await message.answer("Превью включено!", reply_markup=admin_panel_keyboard())
    
async def preview_off(message: Message):

    handlers.remove(Preview())
        
    await message.answer("Превью выключено!", reply_markup=admin_panel_keyboard())

async def user_amount(message: Message):
        
    users = sql.get_all_users()
    await message.answer(f"Количество пользователей: {len(users)}")
    
async def send_all(message: Message):
    #берем сообщение после для рассылки
    mess = message.text.split("\n", 1)[1]
    
    #принимаем массив кортежей из бд
    users = sql.get_all_users()
    
    #рассылаем
    for user in users:
        try:
            await bot.send_message(user[0], mess)
        except Exception as e:
            print(f"Ошибка рассылки юзеру: {e}")
                
async def admin_panel(message: Message):

    await message.answer(f"{message.chat.first_name}, добро пожаловать в админ панель!", reply_markup = admin_panel_keyboard())            
        
async def adding_admin(message: Message):

    sql.set_status(message.from_id, "adding admin")

    await message.answer("Введите id нового администратора:")

async def added_admin(message: Message):

    sql.set_status(message.from_id, "0")

    ADMINS.append(message.text)

    await message.answer("Админ добавлен!")

async def creating_sending(message: Message):

    sql.set_status(message.from_id, "creating sending")

    await message.answer("Введите текст для рассылки:")

async def created_sending(message: Message):

    sql.set_status(message.from_id, "0")

    users = sql.get_all_users()
    
    #рассылаем
    for user in users:
        try:
            await bot.send_message(user[0], message.text)
        except Exception as e:
            print(f"Ошибка рассылки юзеру: {e}")

    await message.answer("Рассылка создана!")

        