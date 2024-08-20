import logging
import os
from datetime import datetime, timedelta
from decors import log_start_finish, timer
import re


logger = logging.getLogger("main")


class ObsolescenceDeleter:
    def __init__(
            self,
            folder_path: str,
            obsolescence_period: int = 7,
            *,
            date_format: str = "%Y%m%d"):

        self.path = folder_path
        self.brink_date = self._get_brink_date(int(obsolescence_period))
        self.date_format = date_format


    def _get_brink_date(self, days: int):

        date_today = datetime.today()
        period = timedelta(days=days)
        brink = date_today - period
        return brink

    def _get_outdated(self):
        regex = r"^(\d{8})_.+"
        files = list(
            filter(
                lambda name: os.path.isfile(
                    os.path.join(self.path, name)),
                os.listdir(self.path)))

        result = []

        for file in files:
            obj = re.fullmatch(regex, file)
            if obj:
                file_date = datetime.strptime(obj.group(1), self.date_format)
                if file_date < self.brink_date:
                    result.append(file)
        if not result:
            logger.info(f"Устаревших файлов не обнаружено. {self.path}\n")
        return result

    def delete_outdated(self):
        files = self._get_outdated()
        for file in files:
            file_path = self.path + file
            self._delete(file_path)

    @staticmethod
    @timer
    @log_start_finish
    def _delete(file_path):
        """Удаление устаревшего файла"""
        os.remove(file_path)

    def __str__(self):

        folder = self.path.split("\\")[-1]

        date_str = self.brink_date.strftime(self.date_format)
        view = f"Deleter<{folder}\\{date_str}>"
        return view
