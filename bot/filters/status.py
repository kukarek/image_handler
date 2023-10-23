from misc.main_config import ADMINS, ON_OFF, THREADS, COUNTRY
from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from database import sql

class isAdmin(BoundFilter):

    async def check(self, message: types.Message) -> bool:

        for admin in ADMINS:
            if admin == message.from_id:
                return True
        return False
    
class isUser(BoundFilter):
    """ 
    Все, кто не админы - юзеры
    """
    async def check(self, message: types.Message) -> bool:

        for admin in ADMINS:
            if admin == message.from_id:
                return False
        return True
    
class botEnable(BoundFilter):

    async def check(self, message: types.Message) -> bool:

        return True if ON_OFF == "On" else False

class botDisable(BoundFilter):

    async def check(self, message: types.Message) -> bool:

        return True if ON_OFF == "Off" else False
    
class user_isNone(BoundFilter):

    async def check(self, message: types.Message) -> bool:

        return True if sql.get_status(message.from_id)[0] == "0" else False

class user_isStart(BoundFilter):

    async def check(self, message: types.Message) -> bool:

        return True if sql.get_status(message.from_id)[0] == "start" else False
    
class user_isWork(BoundFilter):

    async def check(self, message: types.Message) -> bool:

        return True if sql.get_status(message.from_id)[0] == "work" or sql.get_status(message.from_id)[0] == "FRANCE" else False
    
class isAddingAdmin(BoundFilter):

    async def check(self, message: types.Message) -> bool:

        return True if sql.get_status(message.from_id)[0] == "adding admin" else False

class isCreatingSending(BoundFilter):

    async def check(self, message: types.Message) -> bool:

        return True if sql.get_status(message.from_id)[0] == "creating sending" else False
    
class Huge_Pressure(BoundFilter):

    async def check(self, message: types.Message) -> bool:

        return True if len(THREADS) > 10 else False
    
class Incorrect_Country(BoundFilter):

    async def check(self, message: types.Message) -> bool:

        return True if sql.get_country(message.from_id)[0] not in COUNTRY else False
