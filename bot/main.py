import logging
from database import sql
from aiogram import Bot, Dispatcher, executor
from misc.main_config import API_TOKEN

# Установка уровня логирования
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

from .handlers import register_all_handlers

async def __on_start_up(dp: Dispatcher) -> None:

    sql.create_connection()
    register_all_handlers(dp)
    

def start() -> None:

    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)
