from io import BytesIO
from aiogram import F, Dispatcher
from aiogram.types import Message, BufferedInputFile
from aiogram.filters.command import Command
from aiogram.utils.media_group import MediaGroupBuilder
from orm.model import User
from ..keyboards import create_start_keyboard, create_work_keyboard
from image_handler import image_handler
from image_handler.handlers.backgrounds import img_gen
from misc.main_config import COUNTRY
from ..filters.bot_status import THREADS, botDisable, botEnable, Huge_Pressure, Incorrect_Country
from ..filters.admin_status import isAdmin
from ..filters.user_status import IsUser, UserIsWork, UserIsStart, UserIsNone
from log.logger import log

async def start_status_handler(message: Message):

    log.debug(f"Пользователь {message.from_user.id} запустил бота")
    User(message.from_user.id).new()
    text = "Бим бим бам бам\n\nЧто будем лить?"
    await message.answer(text=text, reply_markup=create_start_keyboard(message))

async def return_to_main_menu(message: Message):

    log.debug(f"Пользователь {message.from_user.id} вернулся в главное меню")
    await start_status_handler(message)

async def get_background(message: Message):

    log.debug(f"Пользователь {message.from_user.id} получает фон")

    file_io = BytesIO()
    next(img_gen).save(file_io, format='PNG')
    file_io.seek(0)

    await message.answer_photo(BufferedInputFile(file = file_io.getvalue(), filename="BG_IMG"))
    
async def work_status_handler(message: Message):
    
    log.debug(f"Пользователь {message.from_user.id} пользователь запросил карусель крео")

    country = User(message.from_user.id).get_country()
    COUNTRY[country]["strait"] += 1
    images = image_handler.conversion(country=country)

    THREADS.add()


    media = MediaGroupBuilder()

    for image in images:

        filename = f"image_{images.index(image)}.jpg"

        file_io = BytesIO()
        image.save(file_io, format='PNG')
        file_io.seek(0)
        
        media.add_photo(media = BufferedInputFile(file = file_io.getvalue(), filename = filename))
    
    THREADS.pop()

    await message.answer_media_group(media.build())

async def edit_country(message: Message):

    log.debug(f"Пользователь {message.from_user.id} редактирует страны")

    User(message.from_user.id).set_admin_status("editing country")
    await message.answer("Выберите на клавиатуре:", reply_markup=create_work_keyboard(message))

async def choose_country(message: Message):

    log.debug(f"Пользователь {message.from_user.id} выбирает страну {message.text} для ворка")

    if message.text in COUNTRY:

        User(message.from_user.id).set_status("work")
        User(message.from_user.id).set_country(message.text)
        text = f"Переключаю крео на {message.text}!"
        await message.answer(text=text, reply_markup=create_work_keyboard(message))

    else:
        await message.answer(text="Выберите на клавиатуре")

async def choose_in_keyboard(message: Message):

    await message.answer("Выберите на клавиатуре..")

async def huge_pressure(message: Message):

    log.debug("Большая нагрузка на бота...")
    await message.answer("Большая нагрузка на бота, попробуйте позже...")

async def bot_disable(message: Message):

    log.debug(f"Пользователь {message.from_user.id} пытается воспользоваться ботом, который остановлен админом")
    await message.answer("Бот временно остановлен администратором")

# Регистрация обработчиков в диспетчере
def register_user_handlers(dp: Dispatcher):

    dp.message.register(bot_disable, F.text, IsUser(), botDisable())
    dp.message.register(start_status_handler, Command('start'), botEnable() | isAdmin())
    dp.message.register(start_status_handler, F.text == "Главное меню", botEnable(), UserIsWork())
    dp.message.register(start_status_handler, F.text == "Главное меню", isAdmin(), UserIsWork())

    dp.message.register(start_status_handler, IsUser(), botEnable(), UserIsNone())
    dp.message.register(start_status_handler, isAdmin(), UserIsNone())

    dp.message.register(choose_country, IsUser(), botEnable(), UserIsStart())
    dp.message.register(choose_country, isAdmin(), UserIsStart())

    dp.message.register(huge_pressure, IsUser(), botEnable(), UserIsWork(), Huge_Pressure())
    dp.message.register(huge_pressure, isAdmin(), UserIsWork(), Huge_Pressure())

    dp.message.register(start_status_handler, IsUser(), botEnable(), UserIsWork(), Incorrect_Country())
    dp.message.register(start_status_handler, isAdmin(), UserIsWork(), Incorrect_Country())

    dp.message.register(work_status_handler, F.text == "Получить фото", IsUser(), botEnable(), UserIsWork()) 
    dp.message.register(work_status_handler, F.text == "Получить фото", isAdmin(), UserIsWork())

    dp.message.register(get_background, F.text == "Получить чистый фон", IsUser(), botEnable(), UserIsWork()) 
    dp.message.register(get_background, F.text == "Получить чистый фон", isAdmin(), UserIsWork())

    dp.message.register(choose_in_keyboard, IsUser(), botEnable(), UserIsWork())
    dp.message.register(choose_in_keyboard, isAdmin(), UserIsWork())

    