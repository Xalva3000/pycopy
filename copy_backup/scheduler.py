import logging
from datetime import date

from LEXICON.LEXICON_RU import log_format, log_date_format
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
            "daily": self._daily_actions,
            "once": self._once_actions,
        }

    def _monthly_actions(self,):
        copy_backup = CopyBackup(
            self.destination,
            self.params,
        )

        main_logger.info(f"Файлы для копирования: {copy_backup.files}")

        copy_backup()

        if (
                self.params.save_origin == "NO"
                and copy_backup.files
                and copy_backup.check_size()
        ):
            copy_backup.delete_origin()
            main_logger.info(f"Оригиналы {copy_backup.files} удалены.")
        else:
            main_logger.info(f"Оригиналы сохраняются {copy_backup.files}.")

    def _weekly_actions(self, ):
        # main_logger.info(f"Копирование по расписанию weekly для директории {self.source}")

        copy_backup = CopyBackup(
            self.destination,
            self.params
        )
        main_logger.info(f"Объекты для копирования: {copy_backup.files}\n")

        copy_backup()

        if copy_backup.check_size():

            if self.params.save_origin == "NO":
                copy_backup.delete_origin()
                main_logger.info(f"Оригиналы {copy_backup.files} удалены.")
            else:
                main_logger.info(f"Оригиналы сохраняются {copy_backup.files}.")

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
        file_handler_duplicate.setFormatter(logging.Formatter(fmt=log_format, datefmt=log_date_format))
        logger_duplicate.addHandler(file_handler_duplicate)

        # main_logger.info(f"Копирование по расписанию daily для директории {self.source}")
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
            if self.params.date_format:
                if self.params.save_origin == "NO":
                    deleter_in.delete_outdated()
                deleter_out.delete_outdated()

        logger_duplicate.removeHandler(file_handler_duplicate)

    def _once_actions(self):
        # main_logger.info(f"Копирование по расписанию once для директории {self.source}")

        copy_backup = CopyBackup(
            self.destination,
            self.params
        )

        main_logger.info(f"Объекты для копирования: {copy_backup.files}\n")

        copy_backup()

        if copy_backup.check_size():

            if self.params.save_origin == "NO":
                copy_backup.delete_origin()
                main_logger.info(f"Оригиналы {copy_backup.files} удалены.")
            else:
                main_logger.info(f"Оригиналы {copy_backup.files} сохраняются.")

    def execute(self):
        self.take_actions[self.params.schedule]()
