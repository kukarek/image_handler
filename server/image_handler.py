from PIL import Image
import os
import random
from io import BytesIO
import requests
from config import OVERLAY_FOLDER_FR, OVERLAY_FOLDER_SP, OVERLAY_FOLDER_RM, BACKGROUNDS_LIST, FOOTAGE_FOLDER


def start_combine(country, footage):

    #делаю так, чтобы все 9 фото были либо с футажами либо без
    footage_enable = footage

    if country == "FRANCE":
        overlay_folder = OVERLAY_FOLDER_FR
    if country == "SPAIN":
        overlay_folder = OVERLAY_FOLDER_SP
    if country == "ROMANIA":
        overlay_folder = OVERLAY_FOLDER_RM
    #получение спика фоток для наложения
    overlay_dict = {}

    for filename in os.listdir(overlay_folder):
        # Проверяем, что файл имеет расширение изображения (например, .jpg или .png)
        if filename.endswith((".jpg", ".png")):
            # Формируем полный путь к файлу
            file_path = os.path.join(overlay_folder, filename)
            
            # Загружаем изображение с помощью Pillow
            image = Image.open(file_path)
            
            # Добавляем изображение в словарь, используя имя файла как ключ
            overlay_dict[filename] = image

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

    for overlay in sorted(overlay_dict):
        if i % 2 == 0:
            image = combine(overlay_image=overlay_dict[overlay], background_image=background1, result_name=overlay, footage_enable=footage_enable)
        else:
            image = combine(overlay_image=overlay_dict[overlay], background_image=background2, result_name=overlay, footage_enable=footage_enable)
        i = i + 1
        result_images.append(image)
    
    background1.close()
    background2.close()
    image.close()   

    # Удалите выбранный элемент из массива ссылок
    links.remove(random_link1)
    links.remove(random_link2)

    # Откройте файл для записи и перезапишите его с обновленным списком ссылок
    with open(BACKGROUNDS_LIST, 'w') as file:
        for link in links:
            file.write(link + '\n')

    for image in overlay_dict:
        overlay_dict[image].close()

    return result_images

    



def combine(overlay_image, background_image, result_name, footage_enable):

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
    
    if footage_enable == "On":

        images = os.listdir(FOOTAGE_FOLDER)

        footage = Image.open(f"{FOOTAGE_FOLDER}//{random.choice(images)}")

        # Получаем размеры футажа и фона
        overlay_width, overlay_height = footage.size
        background_width, background_height = result.size

        # Выбираем случайное положение для вставки футажа
        x_position = random.randint(0, overlay_width - background_width)

        # Вырезаем фрагмент из футажа
        crop_box = (x_position, 0, x_position + background_width, background_height)
        overlay_fragment = footage.crop(crop_box)

        # Вставляем фрагмент футажа на фон
        result.paste(overlay_fragment, (0,0), overlay_fragment)
            
        footage.close()
    
    return result

def main():
    start_combine()



if __name__ == "__main__":
    main()