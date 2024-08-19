from tqdm import tqdm
from copy_backup import CopyBackup, ObsolescenceDeleter
from config import groups_of_parameters
from time import sleep
from datetime import date
import logging
import os
from decors import log_start_finish


# создание папки logs для основных логов программы
if "logs" not in os.listdir("."):
    os.mkdir("logs")

# Инициализация логера
main_logger = logging.getLogger("main")

# Создание формата логов
log_format = "[%(asctime)s.%(msecs)03d] %(levelname)6s:  %(message)s"
log_date_format = "%Y-%m-%d %H:%M:%S"

# Получение нужного формата сегодняшней даты
d_today = date.today().strftime("%Y%m%d")

# Создание и настройка StreamHandler
stream_handler = logging.StreamHandler()
main_logger.addHandler(stream_handler)

# Создание и настройка основного FileHandler для записи логов в файл
file_handler = logging.FileHandler(f"logs\\{d_today}_pycopy_logs.txt", encoding="utf-8")
main_logger.addHandler(file_handler)

logging.basicConfig(
    format=log_format,
    datefmt=log_date_format,
    level=logging.DEBUG,
    handlers=[file_handler, stream_handler],
)


@log_start_finish
def main():
    """Основной процесс."""

    for index, param in groups_of_parameters.items():
        source = param["SOURCE_FOLDER"]
        destination = param["DESTINATION_FOLDER"]
        schedule = param["SCHEDULE"]
        save_origin = param["SAVE_ORIGIN"]
        obsolescence_period = param["OBSOLESCENCE_PERIOD"]
        date_format = param["DATE_FORMAT"]
        monthly_schedule_done = False

        # logger_duplicate = logging.getLogger("duplicate_logger")
        file_handler_duplicate = logging.FileHandler(
            destination + f"{d_today}_pycopy_logs.txt",
            mode="a",
            encoding="utf-8",
        )
        main_logger.addHandler(file_handler_duplicate)

        if "monthly" in schedule:
            if date.today().day in range(1, 6) or (
                date.today().day in range(1, 12) and date.today().month == 1
            ):
                # Месячный бэкап
                copy_backup = CopyBackup(
                    source,
                    destination,
                    schedule="monthly",
                    date_format=date_format,
                )
                copy_backup.copy_obj_all()

                if (
                    save_origin == "NO"
                    and copy_backup.files
                    and copy_backup.check_size()
                ):
                    copy_backup.delete_origin()
                monthly_schedule_done = True

        if "weekly" in schedule and not monthly_schedule_done:
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
                    obsolescence_period=obsolescence_period,
                )
                deleter_out = ObsolescenceDeleter(
                    folder_path=copy_backup.destination,
                    obsolescence_period=obsolescence_period,
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
