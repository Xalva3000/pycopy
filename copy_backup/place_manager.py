import logging
import re
import shutil
from datetime import datetime, date, timedelta
import os
from .scheduler import Executor
from param_getter import ParamScheme


logger = logging.getLogger("main")


class PlaceManager:
    def __init__(self, params: ParamScheme):
        self.params = params

        destination_folder = params.destination_folder

        if self.params.schedule == "daily":
            self.destination = destination_folder + "daily\\"
        elif self.params.schedule == "weekly":
            dt = date.today().isoformat() + "\\"
            self.weekly_folder = destination_folder + "weekly\\"
            self.destination = self.weekly_folder + dt
        elif self.params.schedule == "monthly":
            self.monthly_folder = destination_folder + "monthly\\"
            self.destination = self.monthly_folder + date.today().strftime("%Y-%m") + "\\"
        elif self.params.schedule == "once":
            self.once_folder = destination_folder + "once\\"
            self.destination = self.once_folder + date.today().isoformat() + "\\"

    def create_if_not_exists(self):
        logger.info(f"Проверка пути {self.destination}")
        os.makedirs(self.destination, exist_ok=True)
        return self.destination

    def __enter__(self):
        logger.info(f"Копирование по расписанию {self.params.schedule} для директории {self.params.source_folder}")

        self.create_if_not_exists()

        if self.params.schedule == "once":
            for folder in os.listdir(self.once_folder):
                regex = r"\d{4}-\d{2}-\d{2}"
                match = re.fullmatch(regex, folder)
                flag = False
                if match:
                    if date.fromisoformat(folder) < date.today() - timedelta(days=1):
                        flag = True
                else:
                    flag = True
                if flag:
                    logger.info(f"Удаление {self.once_folder + folder}")
                    shutil.rmtree(self.once_folder + folder)

        elif self.params.schedule == "weekly":
            for folder in os.listdir(self.weekly_folder):
                if date.fromisoformat(folder) < date.today() - timedelta(days=30):
                    logger.info(f"Удаление {self.weekly_folder + folder}")
                    shutil.rmtree(self.weekly_folder + folder)

        elif self.params.schedule == "monthly":
            brink_date = datetime.today() - timedelta(days=365)
            for folder in os.listdir(self.monthly_folder):
                regex = r"\d{4}-\d\d"
                match = re.fullmatch(regex, folder)
                if match:
                    folder_date = datetime.strptime(match.string, "%Y-%m")
                    if folder_date <= brink_date:
                        logger.info(f"Удаление {self.monthly_folder + folder}")
                        shutil.rmtree(self.monthly_folder + folder)

        executor = Executor(self.destination, self.params)
        executor.execute()

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info(f"Завершено копирование по расписанию {self.params.schedule} для директории {self.params.source_folder}\n")
