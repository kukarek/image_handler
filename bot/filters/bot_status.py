from misc.main_config import COUNTRY
from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from database import sql


class Threads():

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


class botEnable(BoundFilter):

    async def check(self, message: types.Message) -> bool:

        return True if ON_OFF.status() == "On" else False

class botDisable(BoundFilter):

    async def check(self, message: types.Message) -> bool:

        return True if ON_OFF == "Off" else False
    
class Huge_Pressure(BoundFilter):

    async def check(self, message: types.Message) -> bool:

        return True if THREADS.count() > 10 else False
    
class Incorrect_Country(BoundFilter):

    async def check(self, message: types.Message) -> bool:

        return True if sql.get_country(message.from_id)[0] not in COUNTRY else False


