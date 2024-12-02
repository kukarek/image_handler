from misc.main_config import COUNTRY
from misc.threadmanager import ThreadManager
from misc.toggle import Toggle
from .filter import MyFilter
from aiogram import types
from orm.model import User


class botEnable(MyFilter):

    async def __call__(self, message: types.Message) -> bool:

        return True if Toggle._status() == "On" else False

class botDisable(MyFilter):

    async def __call__(self, message: types.Message) -> bool:

        return True if Toggle == "Off" else False
    
class Huge_Pressure(MyFilter):

    async def __call__(self, message: types.Message) -> bool:

        return True if ThreadManager.countthreads() > 10 else False
    
class Incorrect_Country(MyFilter):

    async def __call__(self, message: types.Message) -> bool:

        return True if User(message.from_user.id).get_country() not in COUNTRY else False


