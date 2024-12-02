from PIL import Image
import os
from .config import handlers
from misc.main_config import COUNTRY

def conversion(country) -> list[Image.Image]:

    #выбор страны
    overlay_folder = COUNTRY[country]["folder"]

    images = get_overlay(overlay_folder)
    
    #запускаем по очереди обработчики фото
    for handler in handlers.get_handlers():
        images = handler.run(images)

    return images


def get_overlay(overlay_folder):
 
    overlays = []

    for filename in sorted(os.listdir(overlay_folder)):
        # Проверяем, что файл имеет расширение изображения (например, .jpg или .png)
        if filename.endswith((".jpg", ".png")):
            # Формируем полный путь к файлу
            file_path = os.path.join(overlay_folder, filename)
            
            # Загружаем изображение с помощью Pillow
            image = Image.open(file_path)
            
            # Добавляем изображение в словарь, используя имя файла как ключ
            overlays.append(image)

    return overlays
