import logging
from datetime import date

from copy_backup import CopyBackup, ObsolescenceDeleter
from param_getter import ParamScheme

main_logger = logging.getLogger("main")
logger_duplicate = logging.getLogger("duplicate_logger")
d_today = date.today().strftime("%Y%m%d")

class Executor:


    def __init__(self, destination, params: ParamScheme):
        self.destination = destination
        self.source = params.source_folder
        self.params = params
        self.take_actions = {
            "monthly": self._monthly_actions,
            "weekly": self._weekly_actions,
            "daily": self._daily_actions
        }

    def _monthly_actions(self,):
        if date.today().day in range(1, 6) or (
                date.today().day in range(1, 12) and date.today().month == 1
        ):
            copy_backup = CopyBackup(
                self.destination,
                self.params
            )
            copy_backup()
            main_logger.info(f"Файлы для копирования: {copy_backup.files}")

            if (
                    self.params.save_origin == "NO"
                    and copy_backup.files
                    and copy_backup.check_size()
            ):
                copy_backup.delete_origin()
            else:
                main_logger.info(f"Оригиналы {copy_backup.files} сохраняются.")

    def _weekly_actions(self, ):
        main_logger.info(f"Копирование по расписанию weekly для директории {self.source}")

        copy_backup = CopyBackup(
            self.destination,
            self.params
        )
        main_logger.info(f"Файлы для копирования: {copy_backup.files}\n")

        copy_backup()

        if copy_backup.check_size():

            if self.params.save_origin == "NO":
                copy_backup.delete_origin()
            else:
                main_logger.info(f"Оригиналы {copy_backup.files} сохраняются.")


    def _daily_actions(self):
        copy_backup = CopyBackup(
            self.destination,
            self.params
        )
        file_handler_duplicate = logging.FileHandler(
            self.destination + f"{d_today}_pycopy_logs.txt",
            mode="a",
            encoding="utf-8",
        )
        logger_duplicate.addHandler(file_handler_duplicate)

        main_logger.info(f"Копирование по расписанию daily для директории {self.source}")
        logger_duplicate.info(f"Копирование по расписанию daily для директории {self.source}")

        main_logger.info(f"Файлы для копирования: {copy_backup.files}\n")
        logger_duplicate.info(f"Файлы для копирования: {copy_backup.files}\n")


        copy_backup()

        if copy_backup.check_size():
            deleter_in = ObsolescenceDeleter(
                folder_path=self.params.source_folder,
                params=self.params,
            )
            deleter_out = ObsolescenceDeleter(
                folder_path=self.destination,
                params=self.params,
            )

            deleter_in.delete_outdated()
            deleter_out.delete_outdated()

        logger_duplicate.removeHandler(file_handler_duplicate)

    def execute(self):
        self.take_actions[self.params.schedule]()
