from PIL import Image
from .handler import Handler
import os
import random
from misc.main_config import FOOTAGE_FOLDER

class Footage(Handler):

    key = "Footage"

    def run(self, images: list[Image.Image]) -> list[Image.Image]:
          
        footages = os.listdir(FOOTAGE_FOLDER)
        
        for image in images:
            
            footage = Image.open(f"{FOOTAGE_FOLDER}//{random.choice(footages)}")

            # Получаем размеры футажа и фона
            overlay_width, overlay_height = footage.size
            background_width, background_height = image.size

            # Выбираем случайное положение для вставки футажа
            x_position = random.randint(0, overlay_width - background_width)

            # Вырезаем фрагмент из футажа
            crop_box = (x_position, 0, x_position + background_width, background_height)
            overlay_fragment = footage.crop(crop_box)

            # Вставляем фрагмент футажа на фон
            image.paste(overlay_fragment, (0,0), overlay_fragment)

        return images