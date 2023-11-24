import logging
from aiogram.types import Message
import time
from aiogram import Dispatcher
from database import sql
from ..main import bot
from ..keyboards.keyboards import admin_panel_keyboard, edit_country_keyboard, config_keyboard
from image_handler.config import handlers
from image_handler.handlers.preview import Preview
from image_handler.handlers.backgrounds import Backgrounds
from image_handler.handlers.footage import Footage
from aiogram.dispatcher.filters import Text
from ..filters.admin_status import *
from ..filters.bot_status import *
from .user_handlers import start_status_handler
from misc.main_config import ADMINS, BACKGROUNDS_LIST, COUNTRY, AVAILABLE_COUNTRYES
from ..filters.bot_status import ON_OFF

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

async def add_backgrounds(message: Message):
    
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

    await message.answer(f"{message.chat.first_name}, добро пожаловать в админ панель!", reply_markup = admin_panel_keyboard(message))            

async def add_admin(message: Message):
    #добавление администратора
    #если команда указана в начале
    if "add" in message.text.split(" ", 1)[0]:
        admin_id = int(message.text.split(" ")[2])
        ADMINS.append(admin_id)
        await message.answer(f"Добавлен администратор с id: {admin_id}")

async def bot_stop(message: Message):
    
    global ON_OFF

    if ON_OFF.status() == "On":
        ON_OFF.OFF()
        await message.answer("Остановка бота", reply_markup=admin_panel_keyboard(message))
    else:
        await message.answer("Бот уже остановлен", reply_markup=admin_panel_keyboard(message))

async def bot_start(message: Message):
    
    global ON_OFF

    if ON_OFF.status() == "Off":
        ON_OFF.ON()
        await message.answer("Запуск бота", reply_markup=admin_panel_keyboard(message))
    else:
        await message.answer("Бот уже запущен", reply_markup=admin_panel_keyboard(message))

async def bot_status(message: Message):

    await message.answer(ON_OFF)

async def config(message: Message):

    sql.set_admin_status(message.from_id, "editing config")

    config = "Текущая настройка:\n"
    for handler in handlers.get_handlers():
        config += f"{handler.key}\n"

    await message.answer(config, reply_markup=config_keyboard(message))

async def footage_on(message: Message):
        
    handlers.append(Footage())

    config = "Текущая настройка:\n"
    for handler in handlers.get_handlers():
        config += f"{handler.key}\n"

    await message.answer(config, reply_markup=config_keyboard(message))
    
async def footage_off(message: Message):

    handlers.remove(Footage())
        
    config = "Текущая настройка:\n"
    for handler in handlers.get_handlers():
        config += f"{handler.key}\n"

    await message.answer(config, reply_markup=config_keyboard(message))

async def background_on(message: Message):
        
    handlers.append(Backgrounds())    

    config = "Текущая настройка:\n"
    for handler in handlers.get_handlers():
        config += f"{handler.key}\n"

    await message.answer(config, reply_markup=config_keyboard(message))
    
async def background_off(message: Message):

    handlers.remove(Backgrounds())
        
    config = "Текущая настройка:\n"
    for handler in handlers.get_handlers():
        config += f"{handler.key}\n"

    await message.answer(config, reply_markup=config_keyboard(message))

async def preview_on(message: Message):
        
    handlers.append(Preview())

    config = "Текущая настройка:\n"
    for handler in handlers.get_handlers():
        config += f"{handler.key}\n"

    await message.answer(config, reply_markup=config_keyboard(message))
    
async def preview_off(message: Message):

    handlers.remove(Preview())
        
    config = "Текущая настройка:\n"
    for handler in handlers.get_handlers():
        config += f"{handler.key}\n"

    await message.answer(config, reply_markup=config_keyboard(message))

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

    sql.set_admin_status(message.from_id, "0")
    await message.answer(f"{message.chat.first_name}, добро пожаловать в админ панель!", reply_markup = admin_panel_keyboard(message))            
        
async def adding_admin(message: Message):

    sql.set_status(message.from_id, "adding admin")

    await message.answer("Введите id нового администратора:")

async def added_admin(message: Message):

    sql.set_status(message.from_id, "0")

    ADMINS.append(message.text)

    await message.answer("Админ добавлен!")

async def creating_sending(message: Message):

    sql.set_admin_status(message.from_id, "creating sending")

    await message.answer("Введите текст для рассылки:")

async def created_sending(message: Message):

    sql.set_admin_status(message.from_id, "0")

    users = sql.get_all_users()
    
    #рассылаем
    for user in users:
        try:
            await bot.send_message(user[0], message.text)
        except Exception as e:
            print(f"Ошибка рассылки юзеру: {e}")

    await message.answer("Рассылка создана!")

async def edit_country(message: Message):

    sql.set_admin_status(message.from_id, "editing country")
    await message.answer("Выберите на клавиатуре:", reply_markup=edit_country_keyboard(message))

async def editing_country(message: Message):

    task = message.text.split(" ")[0]
    country = message.text.split(" ")[1]

    if country in AVAILABLE_COUNTRYES():

        if task == "Включить":

            COUNTRY[country] = {
                            "folder": f"image_handler/overlay_{country}",
                            "strait": 0 }
        else:
            del COUNTRY[country]
            
        await message.answer("Изменения применены!", reply_markup=edit_country_keyboard(message))

    else:
        await message.answer("Выберите на клавиатуре:", reply_markup=edit_country_keyboard(message))

async def edit_config(message: Message):

    sql.set_admin_status(message.from_id, "editing config")
    await message.answer("Выберите на клавиатуре:", reply_markup=config_keyboard(message))



def register_admin_handlers(dp: Dispatcher):

    dp.register_message_handler(start_status_handler, isAdmin(), Text(equals='Главное меню'))
    dp.register_message_handler(admin_panel, isAdmin(), Text(equals='Админ панель'))
    dp.register_message_handler(count, isAdmin(), Text(equals='Количество фонов'))
    dp.register_message_handler(stats, isAdmin(), Text(equals='Статистика пролива'))
    dp.register_message_handler(add_backgrounds, isAdmin(), content_types=[types.ContentType.DOCUMENT])
    dp.register_message_handler(help, isAdmin(), commands=['help'])
    dp.register_message_handler(user_amount, Text(equals="Количество пользователей") & isAdmin())

    dp.register_message_handler(adding_admin, Text(equals="Добавить администратора") & isAdmin())
    dp.register_message_handler(added_admin, isAdmin() & isAddingAdmin())
    dp.register_message_handler(add_admin, Text(startswith="Добавить администратора") & isAdmin())

    dp.register_message_handler(bot_stop, Text(equals="Остановить бота") & isAdmin())
    dp.register_message_handler(bot_start, Text(equals="Запустить бота") & isAdmin())
    dp.register_message_handler(bot_status, Text(equals="Статус бота") & isAdmin())

    dp.register_message_handler(config, Text(equals="Конфиг") & isAdmin())
    dp.register_message_handler(footage_on, Text(equals="Включить футажи") & isAdmin() & Editing_Config())
    dp.register_message_handler(footage_off, Text(equals="Выключить футажи") & isAdmin() & Editing_Config())
    dp.register_message_handler(background_on, Text(equals="Включить фон") & isAdmin() & Editing_Config())
    dp.register_message_handler(background_off, Text(equals="Выключить фон") & isAdmin() & Editing_Config())
    dp.register_message_handler(preview_on, Text(equals="Включить превью") & isAdmin() & Editing_Config())
    dp.register_message_handler(preview_off, Text(equals="Выключить превью") & isAdmin() & Editing_Config())
    dp.register_message_handler(admin_panel, Text(equals="Завершить") & isAdmin() & Editing_Config())

    dp.register_message_handler(creating_sending, Text(equals="Рассылка") & isAdmin())
    dp.register_message_handler(created_sending, isAdmin() & isCreatingSending())
    dp.register_message_handler(send_all, Text(startswith="Рассылка") & isAdmin())

    dp.register_message_handler(edit_country, Text(equals="Редактировать страны") & isAdmin())
    dp.register_message_handler(editing_country, (Text(startswith="Включить") | Text(startswith="Выключить")) & isAdmin() & Editing_Country())
    dp.register_message_handler(admin_panel, Text(equals="Завершить") & isAdmin() & Editing_Country())

    dp.register_message_handler(edit_country, Text(equals="Редактировать фото") & isAdmin())
    dp.register_message_handler(editing_country, (Text(startswith="Включить") | Text(startswith="Выключить")) & isAdmin() & Editing_Country())
    dp.register_message_handler(admin_panel, Text(equals="Завершить") & isAdmin() & Editing_Country())