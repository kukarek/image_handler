import logging
import os

def setup_logger(name):
    # Создание директории для логов, если она не существует
    log_directory = 'log'
    os.makedirs(log_directory, exist_ok=True)
    
    # Настройка логирования
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Установите уровень логирования

    # Создание обработчика для записи логов в файл
    file_handler = logging.FileHandler(os.path.join(log_directory, 'log.log'), encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)  # Установите уровень для обработчика

    # Создание форматтера и добавление его в обработчик
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Добавление обработчика к логгеру
    logger.addHandler(file_handler)

    return logger

log = setup_logger("main_logger")