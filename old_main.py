from copy_backup import CopyBackup, ObsolescenceDeleter

from time import sleep
from datetime import date
import logging
import os
from decors import log_start_finish


# создание папки logs для основных логов программы
if "logs" not in os.listdir("."):
    os.mkdir("logs")

# Инициализация логера
root_logger = logging.getLogger()
# root_logger.propagate = False

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
main_logger.addHandler(stream_handler)


# Создание и настройка основного FileHandler для записи логов в файл
file_handler = logging.FileHandler(f"logs\\{d_today}_pycopy_logs.txt", encoding="utf-8")
main_logger.addHandler(file_handler)




@log_start_finish
def main():
    """Экземпляр программы py-copy."""
    from config import groups_of_parameters

    for index, param in groups_of_parameters.items():
        source = param["SOURCE_FOLDER"]
        destination = param["DESTINATION_FOLDER"]
        mode = param["COPY_FILES_OR_TREE"]
        schedule = param["SCHEDULE"]
        save_origin = param["SAVE_ORIGIN"]
        obsolescence_period = param["OBSOLESCENCE_PERIOD"]
        trigger = param["TRIGGER"]
        monthly_schedule_done = False

        if "monthly" in schedule:
            if date.today().day in range(1, 6) or (
                date.today().day in range(1, 12) and date.today().month == 1
            ):
                main_logger.info(f"Копирование по расписанию monthly для директории {source}")
                # logger_duplicate.info(f"Копирование по расписанию monthly для директории {source}")
                # Месячный бэкап
                copy_backup = CopyBackup(
                    source,
                    destination,
                    schedule="monthly",
                    mode=mode,
                    trigger=trigger,
                )
                copy_backup.copy_obj_all()

                main_logger.info(f"Файлы для копирования: {copy_backup.files}")
                # logger_duplicate.info(f"Файлы для копирования: {copy_backup.files}")

                if (
                    save_origin == "NO"
                    and copy_backup.files
                    and copy_backup.check_size()
                ):
                    if mode == "FILES":
                        copy_backup.copy_obj_all()
                    elif mode == "TREE":
                        copy_backup.copy_tree()
                else:
                    main_logger.info(f"Оригиналы {copy_backup.files} сохраняются.")
                    # logger_duplicate.info(f"Оригиналы {copy_backup.files} не удаляются")

                monthly_schedule_done = True

        if "weekly" in schedule and not monthly_schedule_done:
            main_logger.info(f"Копирование по расписанию weekly для директории {source}")
            # logger_duplicate.info(f"Копирование по расписанию weekly для директории {source}")
            # Недельный бэкап
            copy_backup = CopyBackup(
                source,
                destination,
                schedule="weekly",
                mode=mode,
                dt_format=
                trigger=trigger,
            )
            main_logger.info(f"Файлы для копирования: {copy_backup.files}\n")
            # logger_duplicate.info(f"Файлы для копирования: {copy_backup.files}")
            if copy_backup.files:
                if mode == "FILES":
                    copy_backup.copy_obj_all()
                elif mode == "TREE":
                    copy_backup.copy_tree()

                if copy_backup.check_size():

                    if save_origin == "NO":
                        copy_backup.delete_origin()
                    else:
                        main_logger.info(f"Оригиналы {copy_backup.files} сохраняются.")
                        # logger_duplicate.info(f"Оригиналы {copy_backup.files} не удаляются")

        if "daily" in schedule:

            # инициализация объекта копировщика
            copy_backup = CopyBackup(
                source,
                destination,
                schedule="daily",
                mode=mode,
                trigger=trigger,
            )
            file_handler_duplicate = logging.FileHandler(
                copy_backup.destination + f"{d_today}_pycopy_logs.txt",
                mode="a",
                encoding="utf-8",
            )
            logger_duplicate.addHandler(file_handler_duplicate)

            main_logger.info(f"Копирование по расписанию daily для директории {source}")
            logger_duplicate.info(f"Копирование по расписанию daily для директории {source}")

            main_logger.info(f"Файлы для копирования: {copy_backup.files}\n")
            logger_duplicate.info(f"Файлы для копирования: {copy_backup.files}\n")
            # копирование всего содержащегося в исходной папке,
            # чего нет в папке назначении
            if mode == "FILES":
                if copy_backup.files:
                    copy_backup.copy_obj_all()

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

            elif mode == "TREE":
                if copy_backup.files:
                    copy_backup.copy_tree()
                    copy_backup.check_size()

            # Сверка размеров копий с оригиналами
            # Удаление устаревших файлов


            logger_duplicate.removeHandler(file_handler_duplicate)


# Запуск основной функции
if __name__ == "__main__":

    main()
    try:

        # сообщение в терминал о завершении
        print("\nПрограмма завершила работу. Ожидание 10с. Ctrl+С - выход.")
        # визуальное оформление ожидания
        for i in range(10):
            sleep(1)
    except KeyboardInterrupt:
        print("\nПока!")
        sleep(1)
