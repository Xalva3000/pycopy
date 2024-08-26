import logging
import os
from datetime import datetime, timedelta
from decors import log_start_finish, timer
import re

from param_getter import ParamScheme

logger = logging.getLogger("main")


class ObsolescenceDeleter:
    def __init__(
            self,
            folder_path: str,
            params: ParamScheme):

        self.params = params
        self.path = folder_path
        self.brink_date = self._get_brink_date(int(params.obsolescence_period))
        self.date_format = params.date_code
        self.date_regex = params.date_regex


    def _get_brink_date(self, days: int):
        date_today = datetime.today()
        period = timedelta(days=days)
        brink = date_today - period
        return brink

    def _get_outdated(self):
        if self.params.copy_files_or_tree == "FILES":
            names = list(
                filter(
                    lambda name: os.path.isfile(
                        os.path.join(self.path, name)),
                    os.listdir(self.path)))
        else:
            names = list(
                filter(
                    lambda name: os.path.isdir(
                        os.path.join(self.path, name)),
                    os.listdir(self.path)))

        outdated = []

        for name in names:
            obj = re.fullmatch(self.date_regex, name)
            if obj:
                file_date = datetime.strptime(obj.group(1), self.date_format)
                if file_date < self.brink_date:
                    outdated.append(name)
        if not outdated:
            logger.info(f"Устаревших файлов не обнаружено. {self.path}\n")
        return outdated

    def delete_outdated(self):
        outdated = self._get_outdated()
        for file in outdated:
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
