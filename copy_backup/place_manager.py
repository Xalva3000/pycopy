import logging
from datetime import date
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
            dt = date.today()
            dm = dt.strftime("%d-%m") + "\\"
            m = dt.strftime("%m") + "\\"
            self.destination = destination_folder + "weekly\\" + m + dm
        elif self.params.schedule == "monthly":
            self.destination = destination_folder + "monthly\\" + date.today().strftime("%Y-%m") + "\\"
        elif self.params.schedule == "once":
            self.destination = destination_folder + "once\\"

    def create_if_not_exists(self):
        os.makedirs(self.destination, exist_ok=True)
        return self.destination

    def remove_similar(self, lst):
        for file_name in lst:
            os.remove(self.destination + file_name)


    def __enter__(self):
        logger.info(f"Копирование по расписанию {self.params.schedule} для директории {self.params.source_folder}")
        self.create_if_not_exists()
        # if self.params.copy_files_or_tree == "TREE":
        #     self.remove_similar()
        executor = Executor(self.destination, self.params)
        executor.execute()


    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info(f"Копирование по расписанию {self.params.schedule} для директории {self.params.source_folder}")