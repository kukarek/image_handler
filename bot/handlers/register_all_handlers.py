from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from ..filters import *
from .user_handlers import *
from .admin_handlers import *

def register_all_handlers(dp: Dispatcher):

    dp.register_message_handler(start_status_handler, isAdmin(), Text(equals='Главное меню'))
    dp.register_message_handler(admin_panel, isAdmin(), Text(equals='Админ панель'))
    dp.register_message_handler(count, isAdmin(), Text(equals='Количество фонов'))
    dp.register_message_handler(stats, isAdmin(), Text(equals='Статистика пролива'))
    dp.register_message_handler(add_backgrounds, isAdmin(), content_types=[types.ContentType.DOCUMENT])
    dp.register_message_handler(help, isAdmin(), commands=['help'])
    dp.register_message_handler(adding_admin, Text(equals="Добавить администратора") & isAdmin())
    dp.register_message_handler(added_admin, isAdmin() & isAddingAdmin())
    dp.register_message_handler(add_admin, Text(startswith="Добавить администратора") & isAdmin())
    dp.register_message_handler(bot_stop, Text(equals="Остановить бота") & isAdmin())
    dp.register_message_handler(bot_start, Text(equals="Запустить бота") & isAdmin())
    dp.register_message_handler(bot_status, Text(equals="Статус бота") & isAdmin())
    dp.register_message_handler(config, Text(equals="Конфиг") & isAdmin())
    dp.register_message_handler(footage_on, Text(equals="Включить футажи") & isAdmin())
    dp.register_message_handler(footage_off, Text(equals="Выключить футажи") & isAdmin())
    dp.register_message_handler(background_on, Text(equals="Включить фон") & isAdmin())
    dp.register_message_handler(background_off, Text(equals="Выключить фон") & isAdmin())
    dp.register_message_handler(preview_on, Text(equals="Включить превью") & isAdmin())
    dp.register_message_handler(preview_off, Text(equals="Выключить превью") & isAdmin())
    dp.register_message_handler(user_amount, Text(equals="Количество пользователей") & isAdmin())
    dp.register_message_handler(creating_sending, Text(equals="Рассылка") & isAdmin())
    dp.register_message_handler(created_sending, isAdmin() & isCreatingSending())
    dp.register_message_handler(send_all, Text(startswith="Рассылка") & isAdmin())

    dp.register_message_handler(bot_disable, isUser() & botDisable())
    dp.register_message_handler(start_status_handler, isUser() & botEnable() | isAdmin(), commands=['start'])
    dp.register_message_handler(start_status_handler, isUser() & botEnable() & user_isWork() | isAdmin() & user_isWork(), Text(equals="Главное меню"))
    dp.register_message_handler(start_status_handler, isUser() & botEnable() & user_isNone() | isAdmin() & user_isNone())
    dp.register_message_handler(choose_country, isUser() & botEnable() & user_isStart() | isAdmin() & user_isStart())
    dp.register_message_handler(huge_pressure, isUser() & botEnable() & user_isWork() & Huge_Pressure() | isAdmin() & user_isWork() & Huge_Pressure())
    dp.register_message_handler(start_status_handler, isUser() & botEnable() & user_isWork() & Incorrect_Country() | isAdmin() & user_isWork(), Text(equals="Получить фото"))
    dp.register_message_handler(work_status_handler, isUser() & botEnable() & user_isWork() | isAdmin() & user_isWork(), Text(equals="Получить фото"))
    dp.register_message_handler(choose_in_keyboard, isUser() & botEnable() & user_isWork() | isAdmin() & user_isWork())

