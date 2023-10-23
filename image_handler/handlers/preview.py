from PIL import Image
import os
from .handler import Handler
import random
from misc.main_config import PREVIEW_FOLDER


class Preview(Handler):
    """
    Добавляем в начало карусели превью изображение
    """

    key = "Preview"

    def run(self, images: list[Image.Image]) -> list[Image.Image]:
        
        filename = random.choice(os.listdir(PREVIEW_FOLDER))

        # Формируем полный путь к файлу
        file_path = os.path.join(PREVIEW_FOLDER, filename)
        
        # Загружаем изображение с помощью Pillow
        image = Image.open(file_path)

        # Получаем размеры исходного изображения
        original_width, original_height = image.size

        # Вычисляем соотношение сторон и центрируем обрезку
        aspect_ratio = original_width / original_height
        target_aspect_ratio = 930 / 1080

        if aspect_ratio > target_aspect_ratio:
            # Обрезка боковых краев
            new_width = int(original_height * target_aspect_ratio)
            left = (original_width - new_width) / 2
            right = left + new_width
            image = image.crop((left, 0, right, original_height))
        else:
            # Обрезка верхних и нижних краев
            new_height = int(original_width / target_aspect_ratio)
            top = (original_height - new_height) / 2
            bottom = top + new_height
            image = image.crop((0, top, original_width, bottom))

        # Изменяем размер изображения до целевых размеров
        image = image.resize((1200, 1620), Image.LANCZOS)
        images.insert(0, image)

        return images