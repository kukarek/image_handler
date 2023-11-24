from image_handler.handlers.preview import Preview
from image_handler.handlers.backgrounds import Backgrounds
from image_handler.handlers.footage import Footage
from .handlers.handler import Handler


class Handlers:

    __handlers: list[Handler] = [
        Backgrounds()
    ]

    def get_handlers(self):
        return self.__handlers

    def check(self, handler: Handler) -> bool:
        
        for my_handler in self.__handlers:

            if handler.key == my_handler.key:
                return True
            
        return False

    def append(self, handler: Handler) -> None:
        
        if self.check(handler):
            return
        
        self.__handlers.append(handler)

    def remove(self, handler: Handler) -> None:
       
        if not self.check(handler):
            return
       
        for obj in self.__handlers:
            if handler.key == obj.key:
                self.__handlers.remove(obj)

handlers = Handlers()

