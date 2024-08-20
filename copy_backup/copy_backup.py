import logging
import os
from datetime import date
import shutil
# import subprocess
from LEXICON import SUPPORTED_DATE_FORMATS

from copy_backup.searcher import Searcher
from decors import log_start_finish, timer, log_start

logger1 = logging.getLogger("main")
logger2 = logging.getLogger("duplicate_logger")



class CopyBackup:
    """Объект содержащий методы копирования файлов
    и проверки результатов копирования.

    :source_folder:: строка, путь к папке содержащей исходные файлы
    :destination_folder:: строка, путь к папке назначения
    :schedule:: расписание daily/weekly/monthly"""
    def __init__(
            self,
            source_folder: str,
            destination_folder: str,
            schedule: str,
            mode: str = "FILES",
            trigger="YYYYMMDD",
    ):
        self.schedule = schedule
        self.source = source_folder

        if self.schedule == "daily":
            self.destination = destination_folder + "daily\\"
        elif self.schedule == "weekly":
            self.destination = destination_folder + "weekly\\" + date.today().strftime("%d-%m") + "\\"
        elif self.schedule == "monthly":
            self.destination = destination_folder + "monthly\\" + date.today().strftime("%Y-%m") + "\\"
        elif self.schedule == "once":
            self.destination = destination_folder + "once\\"

        os.makedirs(self.destination, exist_ok=True)

        searcher = Searcher(
            source_folder,
            self.destination,
            mode,
            trigger
        )

        if trigger in SUPPORTED_DATE_FORMATS:
            self.files = searcher.get_latest_difference()
        else:
            self.files = searcher.get_triggered_names()





    @staticmethod
    def dated_name(file_name: str) -> str:
        """Добавляет дату в имя файла-копии."""
        name_parts = file_name.split('.')
        dated_name = name_parts[0] + f"-{date.today()}." + name_parts[1]
        return dated_name

    def copy_obj_all(self, *, max_size=1000000):
        """Цикл применения функции копирования
        ко всем элементам начального списка файлов.
        + указывается размер буфера"""
        for file in self.files:
            source = self.source + file
            destination = self.destination + file
            self.copy_obj(source, destination)

    @staticmethod
    @timer
    @log_start_finish
    def copy_obj(source, destination):
        """Копирование файлового объекта"""
        try:
            with open(source, 'rb') as file_in:
                with open(destination, 'wb') as file_out:
                    shutil.copyfileobj(file_in, file_out)
        except Exception as e:
            logger1.error(f"Ошибка при копировании файлового объекта. Содержание:{e}",
                         exc_info=e)
            logger2.error(f"Ошибка при копировании файлового объекта. Содержание:{e}",
                          exc_info=e)

    @timer
    @log_start_finish
    def copy_tree(self):
        """Копирование директории."""
        try:

            for folder in self.files:
                full_destination_path = self.destination + folder
                if not os.path.exists(full_destination_path):
                    full_source_path = self.source + folder
                    shutil.copytree(full_source_path, full_destination_path)

        except Exception as e:
            logger1.error(f"Ошибка при копировании директории. Содержание:{e}",
                          exc_info=e)
            logger2.error(f"Ошибка при копировании директории. Содержание:{e}",
                          exc_info=e)

    @timer
    @log_start_finish
    def check_size(self):
        """Сверка размера копии"""
        for file in self.files:
            try:
                source = self.source + file
                copy = self.destination + file
                source_size = os.path.getsize(source)
                copy_size = os.path.getsize(copy)
                if source_size == copy_size:
                    logger1.info(f"Исходный файл и копия одинаковы по размеру. {(source, source_size, copy, copy_size)}")
                    logger2.info(
                        f"Исходный файл и копия одинаковы по размеру. {(source, source_size, copy, copy_size)}")
                else:
                    logger1.warning(f"Исходный файл и копия отличаются по размеру. {(source, source_size, copy, copy_size)}")
                    logger2.warning(
                        f"Исходный файл и копия отличаются по размеру. {(source, source_size, copy, copy_size)}")
                    return False
            except Exception as e:
                logger1.error(f"Ошибка при выполнении сверки размеров файла. Содержание {e}",
                             exc_info=e)
                logger2.error(f"Ошибка при выполнении сверки размеров файла. Содержание {e}",
                             exc_info=e)
        return True

    @timer
    @log_start_finish
    def delete_origin(self):
        """Удаление оригинала"""
        for file in self.files:
            try:
                path = self.source + file
                os.remove(path)
                logger1.info(f'Файл {path} удален')
                logger2.info(f'Файл {path} удален')
            except Exception as e:
                logger1.error(f"Ошибка при удалении. Содержание:{e}",
                             exc_info=e)
                logger2.error(f"Ошибка при удалении. Содержание:{e}",
                             exc_info=e)

    def __str__(self):
        return f"Copybackup<{','.join(self.files)}>"

    def __repr__(self):
        return f"Copybackup<{self.files}>"


    # def copy_subproc_all(self):
    #     """Цикл применения создания подпроцесса копирования
    #     ко всем элементам начального списка файлов"""
    #     for file in self.files:
    #         source = self.source + file
    #         destination = self.destination + file
    #         self.copy_subproc(source, destination)
    #
    # @staticmethod
    # @timer
    # @log_start_finish
    # def copy_subproc(source, destination):
    #     """Копирование подпроцессом"""
    #     try:
    #         subprocess.run(['copy',  source, destination], shell=True, check=True)
    #     except subprocess.CalledProcessError as e:
    #         logger.error(f"Ошибка ОС при копировании подпроцессом. Содержание:{e}",
    #                      exc_info=e)
    #     except Exception as e:
    #         logger.error(f"Ошибка при копировании подпроцессом. Содержание:{e}",
    #                      exc_info=e)