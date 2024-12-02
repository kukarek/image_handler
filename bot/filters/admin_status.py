from misc.main_config import ADMINS
from .filter import MyFilter
from orm.model import User
from aiogram import types

class isAdmin(MyFilter):

    async def __call__(self, message: types.Message) -> bool:
        for admin in ADMINS:
            if admin == message.from_user.id:
                return True
        return False

class isAddingAdmin(MyFilter):

    async def __call__(self, message: types.Message) -> bool:

        return True if User(message.from_user.id).get_admin_status() == "adding admin" else False

class isCreatingSending(MyFilter):

    async def __call__(self, message: types.Message) -> bool:

        return True if User(message.from_user.id).get_admin_status() == "creating sending" else False
    
class Editing_Country(MyFilter):

    async def __call__(self, message: types.Message) -> bool:

        return True if User(message.from_user.id).get_admin_status() == "editing country" else False 
    
class Editing_Config(MyFilter):

    async def __call__(self, message: types.Message) -> bool:

        return True if User(message.from_user.id).get_admin_status() == "editing config" else False 