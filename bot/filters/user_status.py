from .filter import MyFilter
from orm.model import User
from aiogram import types
from misc.main_config import ADMINS

class IsUser (MyFilter):
    """ 
    Все, кто не админы - юзеры
    """
    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id not in ADMINS

class UserIsNone(MyFilter):
    async def __call__(self, message: types.Message) -> bool:
        return User(message.from_user.id).get_status() == "0"

class UserIsStart(MyFilter):
    async def __call__(self, message: types.Message) -> bool:
        return User(message.from_user.id).get_status() == "start"

class UserIsWork(MyFilter):
    async def __call__(self, message: types.Message) -> bool:
        status = User(message.from_user.id).get_status()
        return status in ["work", "FRANCE"]