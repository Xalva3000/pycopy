import logging
from datetime import date
import os

# создание папки logs для основных логов программы
if "logs" not in os.listdir("."):
    os.mkdir("logs")

# Инициализация логера
main_logger = logging.getLogger("main_logger")


# Создание формата логов
log_format = logging.Formatter('[%(asctime)s.%(msecs)03d] %(levelname)6s:  %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Получение нужного формата сегодняшней даты
d_today = date.today().strftime("%Y%m%d")

# Создание и настройка основного FileHandler для записи логов в файл
file_handler = logging.FileHandler(f'logs\\{d_today}_pycopy_logs.txt', encoding='utf-8')
file_handler.setFormatter(log_format)
main_logger.addHandler(file_handler)

# Создание FileHandler для дублирования логирования в папку назначения
# if DESTINATION_FOLDER:
#     file_handler_duplicate = logging.FileHandler(DESTINATION_FOLDER + f'{d_today}_pycopy_logs.txt', encoding='utf-8')
#     file_handler_duplicate.setFormatter(log_format)
#     main_logger.addHandler(file_handler_duplicate)

# Создание и настройка StreamHandler
# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(log_format)
# main_logger.addHandler(stream_handler)

logging.basicConfig(level=logging.DEBUG)
# print(main_logger.handlers)
