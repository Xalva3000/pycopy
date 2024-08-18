from tqdm import tqdm
from copy_backup import CopyBackup, ObsolescenceDeleter
from config import groups_of_parameters
from time import sleep
from datetime import date

from decors import log_start


@log_start
def main():
    """Запуск программы."""
    for _, param in groups_of_parameters.items():
        source = param["SOURCE_FOLDER"]
        destination = param["DESTINATION_FOLDER"]
        schedule = param["SCHEDULE"]
        save_origin = param["SAVE_ORIGIN"]

        if "monthly" in schedule:
            if (date.today().day in range(1, 6) or (
                date.today().day in range(1, 12) and date.today().month == 1
            )):
                # Месячный бэкап
                copy_backup = CopyBackup(
                    source,
                    destination,
                    mode="monthly",
                )
                copy_backup.copy_obj_all()

        if "weekly" in schedule:
            # Недельный бэкап
            copy_backup = CopyBackup(
                source,
                destination,
                mode="weekly",
            )
            copy_backup.copy_obj_all()

            if save_origin == "NO" and copy_backup.files and copy_backup.check_size():
                copy_backup.delete_origin()

        if "daily" in schedule:
            # инициализация объекта копировщика
            copy_backup = CopyBackup(
                source,
                destination,
                mode="daily",
            )
            # копирование всего содержащегося в исходной папке,
            # чего нет в папке назначении
            copy_backup.copy_obj_all()

            # Сверка размеров копий с оригиналами
            # Удаление устаревших файлов
            if copy_backup.check_size():
                # настройка удаления
                deleter_in = ObsolescenceDeleter(
                    source,
                    obsolescence_period=7
                )
                deleter_out = ObsolescenceDeleter(
                    destination,
                    obsolescence_period=7
                )

                # поиск и удаление устаревших файлов
                deleter_in.delete_outdated()
                deleter_out.delete_outdated()


# Запуск основной функции
if __name__ == "__main__":

    main()

    # сообщение в терминал о завершении
    print("Программа завершила работу. Ожидание 10с. Ctrl+С - выход.")
    # визуальное оформление ожидания
    for i in tqdm(range(10)):
        sleep(1)
