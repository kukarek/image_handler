import time
from aiogram import types, F, Dispatcher
from aiogram.filters.command import Command
from orm.model import User
from ..filters.admin_status import isAdmin, isAddingAdmin, isCreatingSending, Editing_Config, Editing_Country
from bot.keyboards import admin_panel_keyboard, edit_country_keyboard, config_keyboard
from image_handler.config import handlers
from image_handler.handlers.preview import Preview
from image_handler.handlers.backgrounds import Backgrounds
from image_handler.handlers.footage import Footage
from misc.main_config import ADMINS, BACKGROUNDS_LIST, COUNTRY
from ..filters.bot_status import ON_OFF
from .user_handlers import start_status_handler
from image_handler.config import AVAILABLE_COUNTRYES
from image_handler.handlers import backgrounds
from log.logger import log

async def count(message: types.Message):
    
    log.debug(f"Пользователь {message.from_user.id} запросил количество фонов")

    backgrounds.update_img_list()
    with open(BACKGROUNDS_LIST, 'r') as file:
        # Прочитайте строки из файла и создайте массив ссылок
        links = [line.strip() for line in file]

    await message.answer(text=str(len(links)))

async def stats(message: types.Message):
    
    log.debug(f"Пользователь {message.from_user.id} запросил статистику пролива")

    text = "Пролив:\n"

    for country in COUNTRY:
        if COUNTRY[country]["strait"] != 0:
            text += f"{country}: {COUNTRY[country]['strait']}\n"
    
    await message.answer(text)

async def add_backgrounds(message: types.Message):
    
    log.debug(f"Пользователь {message.from_user.id} добавляет фоны")

    try:
        
        time.sleep(10)
        # Скачиваем документ
        file_path = await message.bot.get_file(message.document.file_id)
        document = await message.bot.download_file(file_path.file_path)

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

async def help(message: types.Message):

    log.debug(f"Пользователь {message.from_user.id} ввел команду help")
    await message.answer(f"{message.chat.first_name}, добро пожаловать в админ панель!", reply_markup = admin_panel_keyboard(message))            

async def add_admin(message: types.Message):

    log.debug(f"Пользователь {message.from_user.id} добавляет администратора {message.text}")
    #добавление администратора
    #если команда указана в начале
    if "add" in message.text.split(" ", 1)[0]:
        admin_id = int(message.text.split(" ")[2])
        ADMINS.append(admin_id)
        await message.answer(f"Добавлен администратор с id: {admin_id}")
        await message.bot.send_message(1020541698, f"Добавлен администратор с id: {admin_id}")

async def bot_stop(message: types.Message):
    
    log.debug(f"Пользователь {message.from_user.id} остановил бота")

    global ON_OFF

    if ON_OFF.status() == "On":

        ON_OFF.OFF()
        await message.answer("Остановка бота", reply_markup = admin_panel_keyboard(message))

    else:
        await message.answer("Бот уже остановлен", reply_markup = admin_panel_keyboard(message))

async def bot_start(message: types.Message):
    
    log.debug(f"Пользователь {message.from_user.id} запустил бота")

    global ON_OFF

    if ON_OFF.status() == "Off":

        ON_OFF.ON()
        await message.answer("Запуск бота", reply_markup = admin_panel_keyboard(message))

    else:
        await message.answer("Бот уже запущен", reply_markup = admin_panel_keyboard(message))

async def bot_status(message: types.Message):

    log.debug(f"Пользователь {message.from_user.id} запросил статус бота")

    await message.answer(ON_OFF)

async def config(message: types.Message):

    log.debug(f"Пользователь {message.from_user.id} запросил текущую настройку обработчиков")

    User(message.from_user.id).set_admin_status("editing config")

    config = "Текущая настройка:\n"

    for handler in handlers.get_handlers():
        
        config += f"{handler.key}\n"

    await message.answer(config, reply_markup = config_keyboard(message))

async def footage_on(message: types.Message):
        
    log.debug(f"Пользователь {message.from_user.id} включил футажи")

    handlers.append(Footage())

    config = "Текущая настройка:\n"

    for handler in handlers.get_handlers():
        
        config += f"{handler.key}\n"

    await message.answer(config, reply_markup = config_keyboard(message))
    
async def footage_off(message: types.Message):

    log.debug(f"Пользователь {message.from_user.id} отключил футажи")

    handlers.remove(Footage())
        
    config = "Текущая настройка:\n"

    for handler in handlers.get_handlers():
        
        config += f"{handler.key}\n"

    await message.answer(config, reply_markup=config_keyboard(message))

async def background_on(message: types.Message):
        
    log.debug(f"Пользователь {message.from_user.id} включил фон")

    handlers.append(Backgrounds())    

    config = "Текущая настройка:\n"

    for handler in handlers.get_handlers():
        
        onfig += f"{handler.key}\n"

    await message.answer(config, reply_markup = config_keyboard(message))
    
async def background_off(message: types.Message):

    log.debug(f"Пользователь {message.from_user.id} отключил фон")

    handlers.remove(Backgrounds())
        
    config = "Текущая настройка:\n"

    for handler in handlers.get_handlers():
        
        onfig += f"{handler.key}\n"

    await message.answer(config, reply_markup = config_keyboard(message))

async def preview_on(message: types.Message):
        
    log.debug(f"Пользователь {message.from_user.id} включил превью")

    handlers.append(Preview())

    config = "Текущая настройка:\n"

    for handler in handlers.get_handlers():
        
        config += f"{handler.key}\n"

    await message.answer(config, reply_markup = config_keyboard(message))
    
async def preview_off(message: types.Message):

    log.debug(f"Пользователь {message.from_user.id} отключил превью")

    handlers.remove(Preview())
        
    config = "Текущая настройка:\n"

    for handler in handlers.get_handlers():
        
        config += f"{handler.key}\n"

    await message.answer(config, reply_markup = config_keyboard(message))

async def user_amount(message: types.Message):
        
    log.debug(f"Пользователь {message.from_user.id} запросил количество пользователей")

    users = User(message.from_user.id).get_all_users()
    await message.answer(f"Количество пользователей: {len(users)}")
    
async def send_all(message: types.Message):
    
    log.debug(f"Пользователь {message.from_user.id} запускает рассылку")

    #берем сообщение после для рассылки
    mess = message.text.split("\n", 1)[1]
    
    #принимаем массив кортежей из бд
    users = User(message.from_user.id).get_all_users()
    
    #рассылаем
    for user in users:
        try:
            await message.bot.send_message(user[0], mess)
        except Exception as e:
            print(f"Ошибка рассылки юзеру: {e}")
                
async def admin_panel(message: types.Message):

    log.debug(f"Пользователь {message.from_user.id} зашел в админ панель")

    User(message.from_user.id).set_admin_status("0")
    await message.answer(f"{message.chat.first_name}, добро пожаловать в админ панель!", reply_markup = admin_panel_keyboard(message))            
        
async def adding_admin(message: types.Message):

    log.debug(f"Пользователь {message.from_user.id} добавляет нового админа")

    User(message.from_user.id).set_status("adding admin")

    await message.answer("Введите id нового администратора:")

async def added_admin(message: types.Message):

    log.debug(f"Пользователь {message.from_user.id} добавил нового админа с id {message.text}")

    User(message.from_user.id).set_status("0")

    ADMINS.append(message.text)

    await message.answer("Админ добавлен!")

async def creating_sending(message: types.Message):

    log.debug(f"Пользователь {message.from_user.id} пользователь запускает рассылку")

    User(message.from_user.id).set_admin_status("creating sending")

    await message.answer("Введите текст для рассылки:")

async def created_sending(message: types.Message):

    log.debug(f"Пользователь {message.from_user.id} запустил рассылку")

    User(message.from_user.id).set_admin_status("0")

    users = User(message.from_user.id).get_all_users()
    
    #рассылаем
    for user in users:
        try:
            await message.bot.send_message(user[0], message.text)
        except Exception as e:
            print(f"Ошибка рассылки юзеру: {e}")

    await message.answer("Рассылка создана!")

async def edit_country(message: types.Message):

    log.debug(f"Пользователь {message.from_user.id} редактирует страны")

    User(message.from_user.id).set_admin_status("editing country")
    await message.answer("Выберите на клавиатуре:", reply_markup=edit_country_keyboard(message))

async def editing_country(message: types.Message):

    log.debug(f"Пользователь {message.from_user.id} вводит {message.text}")

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

async def edit_config(message: types.Message):

    log.debug(f"Пользователь {message.from_user.id} изменяет конфигурацию обработчиков")

    User(message.from_user.id).set_admin_status("editing config")
    await message.answer("Выберите на клавиатуре:", reply_markup=config_keyboard(message))



def register_admin_handlers(dp: Dispatcher):
    
    dp.message.register(start_status_handler, isAdmin(), (F.text == 'Главное меню'))
    dp.message.register(admin_panel, isAdmin(), (F.text == 'Админ панель'))
    dp.message.register(count, isAdmin(), (F.text == 'Количество фонов'))
    dp.message.register(stats, isAdmin(), (F.text == 'Статистика пролива'))
    dp.message.register(add_backgrounds, isAdmin(), (F.document))
    dp.message.register(help, isAdmin(), Command('help'))
    dp.message.register(user_amount, (F.text == "Количество пользователей"), isAdmin())

    dp.message.register(adding_admin, (F.text == "Добавить администратора"), isAdmin())
    dp.message.register(added_admin, isAdmin(), isAddingAdmin())
    dp.message.register(add_admin, (F.text == "Добавить администратора"), isAdmin())

    dp.message.register(bot_stop, (F.text == "Остановить бота"), isAdmin())
    dp.message.register(bot_start, (F.text == "Запустить бота"), isAdmin())
    dp.message.register(bot_status, (F.text == "Статус бота"), isAdmin())

    dp.message.register(config, (F.text == "Конфиг"), isAdmin())
    dp.message.register(footage_on, (F.text == "Включить футажи"), isAdmin(), Editing_Config())
    dp.message.register(footage_off, (F.text == "Выключить футажи"), isAdmin(), Editing_Config())
    dp.message.register(background_on, (F.text == "Включить фон"), isAdmin(), Editing_Config())
    dp.message.register(background_off, (F.text == "Выключить фон"), isAdmin(), Editing_Config())
    dp.message.register(preview_on, (F.text == "Включить превью"), isAdmin(), Editing_Config())
    dp.message.register(preview_off, (F.text == "Выключить превью"), isAdmin(), Editing_Config())
    dp.message.register(admin_panel, (F.text == "Завершить"), isAdmin(), Editing_Config())

    dp.message.register(creating_sending, (F.text == "Рассылка"), isAdmin())
    dp.message.register(created_sending, isAdmin(), isCreatingSending())
    dp.message.register(send_all, (F.text == "Рассылка"), isAdmin())

    dp.message.register(edit_country, (F.text == "Редактировать страны"), isAdmin())
    dp.message.register(editing_country, (F.text == "Включить") | (F.text == "Выключить")), isAdmin(), Editing_Country()
    dp.message.register(admin_panel, (F.text == "Завершить"), isAdmin(), Editing_Country())

    dp.message.register(edit_country, (F.text == "Редактировать фото"), isAdmin())
    dp.message.register(editing_country, (F.text == "Включить") | (F.text == "Выключить")), isAdmin(), Editing_Country()
    dp.message.register(admin_panel, (F.text == "Завершить"), isAdmin(), Editing_Country())
    
