import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message
from aiogram.utils import executor
import image_handler
from io import BytesIO
from aiogram.types import InputMediaPhoto
import time
import sql
import chatbot_logic
from config import API_TOKEN, ADMINS, ON_OFF, IS_ENABLE_FOOTAGE, THREADS, HELP, FR_COUNT, SP_COUNT, RM_COUNT, BACKGROUNDS_LIST

# Установка уровня логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def admin(id):
    for admin in ADMINS:
        if admin == id:
            return True
    return False


@dp.message_handler(commands=['count'])
async def count(message: Message):
    if admin(message.from_id):
        with open(BACKGROUNDS_LIST, 'r') as file:
            # Прочитайте строки из файла и создайте массив ссылок
            links = [line.strip() for line in file]

        await message.answer(text=len(links))

@dp.message_handler(commands=['stats'])
async def count(message: Message):
    if admin(message.from_id):

        country = (f"Пролив по Франции: {FR_COUNT}\n"+
                   f"Пролив по Испании: {SP_COUNT}\n"+
                   f"Пролив по Румынии: {RM_COUNT}\n")


        await message.answer(country)

#счетчик для статистики
def counter(status):

    global FR_COUNT
    global SP_COUNT
    global RM_COUNT

    if status == "FRANCE":
        FR_COUNT += 1
    if status == "SPAIN":
        SP_COUNT += 1
    if status == "ROMANIA":
        RM_COUNT += 1


async def get_photo(message, status):

    if ON_OFF == "On" or admin(message.from_id):
        if len(THREADS) > 10:

            await message.answer("Большая нагрузка на бота, попробуйте позже!")
        else:
            #отслеживание общей нагрузки
            THREADS.append("thread")
            #счетчик для статистики пролива
            counter(status)

            images = image_handler.start_combine(country=status, footage=IS_ENABLE_FOOTAGE)

            if images:

                input_media_images = []
                
                i = 0

                while i < len(images) - 1:
                    image_stream = BytesIO()
                    images[i].save(image_stream, format='JPEG')
                    image_stream.seek(0)
                    input_media_images.append(InputMediaPhoto(media=image_stream)) 
                    i = i + 1   
                print("Фото сгенерированы!")

            await message.answer_media_group(media = input_media_images)
            THREADS.pop()

    else:
        await message.answer("Бот временно остановлен администратором")
    
async def admin_panel(message):

    global ON_OFF
    global IS_ENABLE_FOOTAGE

    if admin(message.from_id):
        #добавление администратора
        if "add" in message.text:
            admin_id = int(message.text.split(" ")[1])
            ADMINS.append(admin_id)
            await message.answer(f"Добавлен администратор с id: {admin_id}")
            return True

        #остановка бота
        elif message.text == "stop":
            if ON_OFF == "On":
                ON_OFF = "Off"
                await message.answer("Остановка бота")
            else:
                await message.answer("Бот уже остановлен")
            return True

        #запуск бота
        elif message.text == "start":
            if ON_OFF == "Off":
                ON_OFF = "On"
                await message.answer("Запуск бота")
            else:
                await message.answer("Бот уже запущен")
            return True

        #статус
        elif message.text == "status":
            
            await message.answer(ON_OFF)
            return True

        elif message.text == "footage":
            
            await message.answer(IS_ENABLE_FOOTAGE)
            return True

        elif message.text == "footage on":
            IS_ENABLE_FOOTAGE = "On"
            await message.answer("Футажи включены!")
            return True
        
        elif message.text == "footage off":
            IS_ENABLE_FOOTAGE = "Off"
            await message.answer("Футажи отключены!")
            return True
        
    return False

@dp.message_handler(commands=['help'])
async def on_start(message: Message):

    if admin(message.from_id):
        await message.answer(HELP)

# Обработчик приема документа
@dp.message_handler(content_types=[types.ContentType.DOCUMENT])
async def process_document(message: types.Message):
    global ON_OFF
    global BACKGROUNDS_LIST
    try:
        #добавление списка фонов
        if admin(message.from_id):
            ON_OFF = "Off"
            time.sleep(10)
            # Скачиваем документ
            file_path = await bot.get_file(message.document.file_id)
            document = await bot.download_file(file_path.file_path)

            # Извлекаем текст из загруженного документа
            document_bytes = document.read()
            new_backgrounds = document_bytes.decode("utf-8")      
            new_backgrounds = new_backgrounds.replace("\r", "") 

            with open(BACKGROUNDS_LIST, "a") as file:
                # Добавляем новый текст с новой строкой
                file.write("\n"+ new_backgrounds)   

            ON_OFF = "On"
            await message.answer(text="Фоны успешно добавлены!")
    except:
        await message.answer("Произошла ошибка")

@dp.message_handler()
async def echo(message: Message):
    global IS_ENABLE_FOOTAGE
    global ON_OFF
    try:

        #если действие было с админ панелью, выходим
        if(await admin_panel(message=message)):
            return
        
        if ON_OFF == "On" or admin(message.from_id):
            #подключаем логику чат-бота
            response, keyboard, status = chatbot_logic.reply_message_handler(user_id=message.from_id, message_text=message.text)

            #если ответ None, значит просто обрабатываем фото
            if response:
                if keyboard:
                    await message.answer(text=response, reply_markup=keyboard)
                else:
                    await message.answer(text=response)
            else:
                await get_photo(message, status)

        else:
            await message.answer("Бот временно остановлен администратором!")

        

    except Exception as e: 
        await message.answer(text=f"Попробуйте позже\n\n{e}")


def main():
    # Запуск бота
    sql.create_connection()
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()