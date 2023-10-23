from PIL import Image
from .handler import Handler
import os
import random
import requests
from io import BytesIO
from misc.main_config import BACKGROUNDS_LIST


class Backgrounds(Handler):

    key = "Backgrounds"

    def run(self, images: list[Image.Image]) -> list[Image.Image]:
        
        #получение рандомной ссылки на фото из списка ссылок фонов
        with open(BACKGROUNDS_LIST, 'r') as file:
            # Прочитайте строки из файла и создайте массив ссылок
            links = [line.strip() for line in file]

        random_link1 = random.choice(links)
        random_link2 = random.choice(links)

        #запрос на получение картинки
        response1 = requests.get(random_link1)
        response2 = requests.get(random_link2)

        background1 = Image.open(BytesIO(response1.content))
        background2 = Image.open(BytesIO(response2.content))


        result_images = []
        i = 1

        for overlay in images:
            if i % 2 == 0:
                image = self.__combine(overlay_image=overlay, background_image=background1)
            else:
                image = self.__combine(overlay_image=overlay, background_image=background2)
            i = i + 1
            result_images.append(image)

        background1.close()
        background2.close()

        # Удалите выбранный элемент из массива ссылок
        links.remove(random_link1)
        links.remove(random_link2)

        return result_images

    def __combine(self, overlay_image, background_image):

        # Получаем размеры изображения
        width, height = background_image.size

        # Вычисляем новые размеры и координаты для вырезки
        new_width = min(width, height * 9 // 16)  # Ширина будет 9/16 от высоты
        new_height = min(height, width * 16 // 9)  # Высота будет 16/9 от ширины
        left = 0  # Начало вырезки по горизонтали
        top = height - new_height  # Начало вырезки по вертикали (снизу)

        # Вырезаем часть изображения
        background_image = background_image.crop((left, top, left + new_width, top + new_height))

        # Меняем размер до 1080x1920
        background_image = background_image.resize((1080, 1920), Image.LANCZOS)

        # Получаем размеры фона и наложения
        background_width, background_height = background_image.size
        overlay_width, overlay_height = overlay_image.size

        # Рассчитываем новые размеры наложения, чтобы оно соответствовало разрешению 1080x1920
        new_overlay_width = 900
        new_overlay_height = int(overlay_height * (new_overlay_width / overlay_width))

        # Масштабируем наложение к новым размерам
        overlay_image = overlay_image.resize((new_overlay_width, new_overlay_height), Image.LANCZOS)

        # Рассчитываем координаты, чтобы разместить наложение в центре фона с рамками
        x = (background_width - new_overlay_width) // 2
        y = (background_height - new_overlay_height) // 2

        # Создаем новое изображение, накладывая фон и наложение
        result = background_image.copy()
        result.paste(overlay_image, (x, y))
        
        return result
    