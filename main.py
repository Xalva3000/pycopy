from tqdm import tqdm
from copy_backup import CopyBackup, ObsolescenceDeleter
from config import groups_of_parameters
from time import sleep
from datetime import date
import logging
import os
from decors import log_start

main_logger = logging.getLogger(__name__)

if "logs" not in os.listdir("."):
    os.mkdir("logs")
# Создание формата логов
log_format = logging.Formatter('[%(asctime)s.%(msecs)03d] %(levelname)6s:  %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Получение нужного формата сегодняшней даты
d_today = date.today().strftime("%Y%m%d")


stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_format)
main_logger.addHandler(stream_handler)

# Создание и настройка основного FileHandler для записи логов в файл
file_handler = logging.FileHandler(f'logs\\{d_today}_pycopy_logs.txt', encoding='utf-8')
file_handler.setFormatter(log_format)
main_logger.addHandler(file_handler)
logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, stream_handler])


@log_start
def main():
    """Запуск программы."""


    for _, param in groups_of_parameters.items():
        source = param["SOURCE_FOLDER"]
        destination = param["DESTINATION_FOLDER"]
        schedule = param["SCHEDULE"]
        save_origin = param["SAVE_ORIGIN"]
        obsolescence_period = param["OBSOLESCENCE_PERIOD"]
        date_format = param["DATE_FORMAT"]

        file_handler_duplicate = logging.FileHandler(destination + f'{d_today}_pycopy_logs.txt',
                                                     encoding='utf-8')
        file_handler_duplicate.setLevel(logging.DEBUG)
        file_handler_duplicate.setFormatter(log_format)
        main_logger.addHandler(file_handler_duplicate)

        if "monthly" in schedule:
            if (date.today().day in range(1, 6) or (
                date.today().day in range(1, 12) and date.today().month == 1
            )):
                # Месячный бэкап
                copy_backup = CopyBackup(
                    source,
                    destination,
                    schedule="monthly",
                    date_format=date_format,
                )
                copy_backup.copy_obj_all()

                if save_origin == "NO" and copy_backup.files and copy_backup.check_size():
                    copy_backup.delete_origin()

        if "weekly" in schedule:
            # Недельный бэкап
            copy_backup = CopyBackup(
                source,
                destination,
                schedule="weekly",
                date_format=date_format,
            )
            copy_backup.copy_obj_all()

            if save_origin == "NO" and copy_backup.files and copy_backup.check_size():
                copy_backup.delete_origin()

        if "daily" in schedule:
            # инициализация объекта копировщика
            copy_backup = CopyBackup(
                source,
                destination,
                schedule="daily",
                date_format=date_format,
            )
            # копирование всего содержащегося в исходной папке,
            # чего нет в папке назначении
            copy_backup.copy_obj_all()

            # Сверка размеров копий с оригиналами
            # Удаление устаревших файлов
            if copy_backup.check_size():
                # настройка удаления
                deleter_in = ObsolescenceDeleter(
                    folder_path=copy_backup.source,
                    obsolescence_period=obsolescence_period
                )
                deleter_out = ObsolescenceDeleter(
                    folder_path=copy_backup.destination,
                    obsolescence_period=obsolescence_period
                )

                # поиск и удаление устаревших файлов
                deleter_in.delete_outdated()
                deleter_out.delete_outdated()
        main_logger.removeHandler(file_handler_duplicate)


# Запуск основной функции
if __name__ == "__main__":

    main()

    # сообщение в терминал о завершении
    print("Программа завершила работу. Ожидание 10с. Ctrl+С - выход.")
    # визуальное оформление ожидания
    for i in tqdm(range(10)):
        sleep(1)
