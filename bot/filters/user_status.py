from misc.main_config import ADMINS
from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from database import sql


class isUser(BoundFilter):
    """ 
    Все, кто не админы - юзеры
    """
    async def check(self, message: types.Message) -> bool:

        for admin in ADMINS:
            if admin == message.from_id:
                return False
        return True
  
class user_isNone(BoundFilter):

    async def check(self, message: types.Message) -> bool:

        return True if sql.get_status(message.from_id)[0] == "0" else False

class user_isStart(BoundFilter):

    async def check(self, message: types.Message) -> bool:

        return True if sql.get_status(message.from_id)[0] == "start" else False
    
class user_isWork(BoundFilter):

    async def check(self, message: types.Message) -> bool:

        return True if sql.get_status(message.from_id)[0] == "work" or sql.get_status(message.from_id)[0] == "FRANCE" else False
    