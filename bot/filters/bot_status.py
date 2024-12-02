from misc.main_config import COUNTRY
from .filter import MyFilter
from aiogram import types
from orm.model import User



class Threads:

    def __init__(self) -> None:
        self.threads = []

    def add(self):
        self.threads.append("Thread")

    def pop(self):
        if self.threads:
            self.threads.pop()

    def count(self):
        return len(self.threads)

THREADS = Threads() 


class On_Off:

    def __init__(self):
        self.__status = "Off"

    def ON(self):
        self.__status = "On"

    def OFF(self):
        self.__status = "Off"

    def status(self):
        return self.__status


ON_OFF = On_Off()


class botEnable(MyFilter):

    async def __call__(self, message: types.Message) -> bool:

        return True if ON_OFF.status() == "On" else False

class botDisable(MyFilter):

    async def __call__(self, message: types.Message) -> bool:

        return True if ON_OFF == "Off" else False
    
class Huge_Pressure(MyFilter):

    async def __call__(self, message: types.Message) -> bool:

        return True if THREADS.count() > 10 else False
    
class Incorrect_Country(MyFilter):

    async def __call__(self, message: types.Message) -> bool:

        return True if User(message.from_user.id).get_country() not in COUNTRY else False


