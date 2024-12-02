from PIL import Image
import logging
from .handler import Handler
import random
import requests
from io import BytesIO
from misc.main_config import BACKGROUNDS_LIST
from log.logger import log
import re

def update_img_list():

    # Читаем лог файл
    with open("log/log.log", mode="r", encoding='utf-8', errors="replace") as file:

        target_line = None
        pattern = r"https.+"
        lines = file.readlines()

        # Ищем целевую строку в обратном порядке
        for line in reversed(lines):
            if "Получение изображения" in line.strip():
                found_lines = re.findall(pattern, line.strip())
                if found_lines:  # Проверяем, что нашлись совпадения
                    target_line = found_lines[0]  # Берем первую найденную строку
                    break

    # Если нашли целевую строку, продолжаем
    if target_line:
        with open(BACKGROUNDS_LIST, mode="r", encoding="utf-8") as f:
            lines = f.readlines()  # Читаем все строки из файла
            target_index = None

            # Находим индекс целевой строки
            for i, line in enumerate(lines):
                if target_line in line:  # Проверяем, содержится ли целевая строка в текущей строке
                    target_index = i
                    break  # Прерываем цикл, если нашли

        # Если нашли индекс, записываем оставшиеся строки обратно в файл
        if target_index is not None:
            with open(BACKGROUNDS_LIST, mode="w", encoding="utf-8") as f:
                f.writelines(lines[target_index + 1:])  # Записываем строки, начиная с найденной

def _image_gen():

    """Генератор, который читает строки из файла и выкидывает картинку в формате PIL."""
    with open(BACKGROUNDS_LIST, 'r', encoding='utf-8') as file:
        for line in file:
            url = line.strip()  # Убираем пробелы и переносы
            if url:  # Проверяем, что строка не пустая
                try:
                    response = requests.get(url)  # Загружаем изображение
                    response.raise_for_status()  # Проверяем на ошибки HTTP
                    log.debug(f"Получение изображения: {url}")
                    yield Image.open(BytesIO(response.content))  # Возвращаем изображение
                except requests.exceptions.RequestException as e:
                    print(f"Ошибка при загрузке изображения: {e}")
                except IOError as e:
                    print(f"Ошибка при открытии изображения: {e}")

img_gen = _image_gen()

class Backgrounds(Handler):

    key = "Backgrounds"

    def run(self, images: list[Image.Image]) -> list[Image.Image]:

        background = next(img_gen)

        result_images = []

        for i, overlay in enumerate(images, start=1):
            image = self.combine(overlay_image=overlay, background_image=background)
            result_images.append(image)
            print(i)  # Печатает индекс (начиная с 1)

        return result_images


    def combine(self, overlay_image, background_image):
        # Получаем размеры фона и наложения
        background_width, background_height = background_image.size
        overlay_width, overlay_height = overlay_image.size

        # Рассчитываем новые размеры наложения
        new_overlay_width = 900
        new_overlay_height = int(overlay_height * (new_overlay_width / overlay_width))

        # Масштабируем наложение к новым размерам
        overlay_image = overlay_image.resize((new_overlay_width, new_overlay_height), Image.LANCZOS)

        # Рассчитываем координаты, чтобы разместить наложение в центре фона
        x = (background_width - new_overlay_width) // 2
        y = (background_height - new_overlay_height) // 2

        # Создаем новое изображение, накладывая наложение на фон
        result = background_image.copy()
        result.paste(overlay_image, (x, y), overlay_image)  # Используем наложение в качестве маски

        return result
