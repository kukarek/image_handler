from aiogram import Bot, Dispatcher
from misc.main_config import API_TOKEN_TEST
from bot.handlers.register_all_handlers import register_all_handlers
import time
from log.logger import log
import logging
import os
from orm.database import sql
from image_handler.handlers.backgrounds import update_img_list


bot = Bot(token=API_TOKEN_TEST)
dp = Dispatcher()

def on_startup() -> None:
    
    logging.getLogger("aiogram").addHandler(logging.FileHandler(os.path.join("log", 'log.log')))
    log.info("--Логирование настроено--")
    register_all_handlers(dp)
    log.info("--Обработчики зарегистрированы--")
    sql.create_db()
    log.info("--База данных подключена--")
    update_img_list()
    log.info("--Список фонов обновлен--")

async def start() -> None:

    on_startup()

    log.info("--запуск бота--")
    try:
        # Запуск бота
        await dp.start_polling(bot)
        
    finally:
        time.sleep(5)
        dp.start_polling(bot)



