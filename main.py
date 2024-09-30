from typing import Optional, List

from LEXICON import LEXICON_RU
from copy_backup import PlaceManager

from time import sleep
from datetime import date
import logging
import os
from decors import log_start_finish
from sys import argv


# создание папки logs для основных логов программы
if "logs" not in os.listdir("."):
    os.mkdir("logs")

# Инициализация логера
root_logger = logging.getLogger()
root_logger.propagate = False

# Создание формата логов
log_format = "[%(asctime)s.%(msecs)03d] %(levelname)6s:  %(message)s"
log_date_format = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    format=log_format,
    datefmt=log_date_format,
)

main_logger = logging.getLogger("main")
main_logger.setLevel(logging.INFO)
main_logger.propagate = False

logger_duplicate = logging.getLogger("duplicate_logger")
logger_duplicate.setLevel(logging.INFO)
logger_duplicate.propagate = False


# Получение нужного формата сегодняшней даты
d_today = date.today().strftime("%Y%m%d")


# Создание и настройка StreamHandler
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter(fmt=log_format, datefmt=log_date_format))
main_logger.addHandler(stream_handler)


# Создание и настройка основного FileHandler для записи логов в файл
file_handler = logging.FileHandler(f"logs\\{d_today}_pycopy_logs.txt", encoding="utf-8")
file_handler.setFormatter(logging.Formatter(fmt=log_format, datefmt=log_date_format))
main_logger.addHandler(file_handler)


@log_start_finish
def main(params, exclude: List[Optional[int]] = None):
    """Экземпляр программы py-copy."""
    exclude = exclude or []
    errors = []

    for index, param in params.items():
        if index not in exclude:
            print(f'Обработка расписания №{index}.')
            try:
                pm = PlaceManager(param)
                # pm.create_if_not_exists()

                with pm:
                    print(f'Обработано расписание №{index}.')

            except Exception as e:
                errors.append({"n": index, "params": param})
                raise Exception


    main_logger.info(f"Ошибок {len(errors)}")

    if errors:
        for i in errors:
            main_logger.info(f"Расписание №{i['n']} не выполнено. Параметры: {i['params']}")



# Запуск основной функции
if __name__ == "__main__":
    from config import param_getter

    params = param_getter.as_schemes

    sleep(0.3)

    for index, param in params.items():
        file_or_folder = "файлов" if param.copy_files_or_tree == "FILES" else "директорий"
        string = f"""Расписание №{index}. Схема {param.schedule}. 
    Поиск {param.substring} {param.date_format} {file_or_folder} в {param.source_folder}
    для копирования в {param.destination_folder}.\n"""
        print(string)
    exclude = []
    if len(argv) == 1:

        appeal = LEXICON_RU["start_copy"]

        exclude = list(map(int, input(appeal).split()))
        if exclude:
            print(f"Следующие расписания будут исключены {exclude}.\n\n")
        sleep(0.5)

    main(params, exclude=exclude)
    try:

        # сообщение в терминал о завершении
        print("\nПрограмма завершила работу. Ожидание 10с. Ctrl+С - выход.")
        # визуальное оформление ожидания
        for i in range(10):
            sleep(1)
    except KeyboardInterrupt:
        print("\nПока!")
        sleep(1)
