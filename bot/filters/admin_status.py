from misc.main_config import ADMINS
from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from database import sql

class isAdmin(BoundFilter):

    async def check(self, message: types.Message) -> bool:

        for admin in ADMINS:
            if admin == message.from_id:
                return True
        return False

class isAddingAdmin(BoundFilter):

    async def check(self, message: types.Message) -> bool:

        return True if sql.get_admin_status(message.from_id)[0] == "adding admin" else False

class isCreatingSending(BoundFilter):

    async def check(self, message: types.Message) -> bool:

        return True if sql.get_admin_status(message.from_id)[0] == "creating sending" else False
    
class Editing_Country(BoundFilter):

    async def check(self, message: types.Message) -> bool:

        return True if sql.get_admin_status(message.from_id)[0] == "editing country" else False 
    
class Editing_Config(BoundFilter):

    async def check(self, message: types.Message) -> bool:

        return True if sql.get_admin_status(message.from_id)[0] == "editing config" else False 