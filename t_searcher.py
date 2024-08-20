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
    """Экземпляр программы pycopy."""
    from config import groups_of_parameters

    for index, param in groups_of_parameters.items():
        source = param["SOURCE_FOLDER"]
        destination = param["DESTINATION_FOLDER"]
        mode = param["COPY_FILES_OR_FOLDER"]
        schedule = param["SCHEDULE"]
        save_origin = param["SAVE_ORIGIN"]
        obsolescence_period = param["OBSOLESCENCE_PERIOD"]
        trigger = param["TRIGGER"]
        monthly_schedule_done = False


        copy_backup = CopyBackup(
            source,
            destination,
            mode="monthly",
            schedule=schedule,
            trigger=trigger,
        )
        print(copy_backup.files)




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
