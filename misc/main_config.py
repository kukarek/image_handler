import os

def AVAILABLE_COUNTRYES():

    countryes = []
    # Указываем путь к папке, которую нужно просканировать
    folder_path = "image_handler"

    # Получаем список всех подпапок в указанной директории
    subfolders = (f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f)))

    # Фильтруем подпапки, оставляем только те, чьи имена начинаются с "overlay"
    overlay_folders = [f for f in subfolders if f.startswith("overlay")]

    for folder in overlay_folders:
        countryes.append(folder.split("_")[1])

    return countryes

COUNTRY = {
    "FRANCE": {
        "folder": "image_handler/overlay_FRANCE",
        "strait": 0,
        "video_folder": "video_handler/video_FRANCE"}
}

BACKGROUNDS_LIST = "image_handler/backgrounds.txt"
PREVIEW_FOLDER = "image_handler/preview"
FOOTAGE_FOLDER = "image_handler/footage"

API_TOKEN_TEST = '6588918438:AAEuWOePbDIWlDufBsnHTku9wj9oHlU5IrQ' 
API_TOKEN = "6516087703:AAFogf1wdiNFFkolsNWMjOvSXj0BN3ypi5g"
#Админы для админ панели
ADMINS = [1020541698, 6356732052]

#база данных 
DB = "database/bot users.db"

