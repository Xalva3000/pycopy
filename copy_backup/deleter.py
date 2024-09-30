import logging
import os
import shutil
from datetime import datetime, timedelta
from decors import log_start_finish, timer
import re

from param_getter import ParamScheme

logger = logging.getLogger("main")


class ObsolescenceDeleter:
    def __init__(
            self,
            folder_path: str,
            params: ParamScheme,
    ):

        self.path = folder_path
        self.params = params
        self.brink_date = self._get_brink_date(int(params.obsolescence_period))
        self.date_format = params.date_code
        self.date_regex = params.date_regex


    def _get_brink_date(self, days: int):
        date_today = datetime.today()
        period = timedelta(days=days)
        brink = date_today - period
        return brink

    def _get_files_or_dirs(self):
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
        return names

    def _get_outdated(self):
        names = self._get_files_or_dirs()

        outdated = []

        for name in names:
            match = re.search(self.date_regex, name.split(".")[0])
            if match:
                _dt = match.group(1) or match.group(2)
                file_date = datetime.strptime(_dt, self.date_format)
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


    @timer
    @log_start_finish
    def _delete(self, path):
        """Удаление устаревшего файла или директории"""
        if self.params.copy_files_or_tree == "FILES":
            os.remove(path)
        else:
            shutil.rmtree(path)

    def __str__(self):
        folder = self.path.split("\\")[-1]

        date_str = self.brink_date.strftime(self.date_format)
        view = f"Deleter<{folder}\\{date_str}>"
        return view

    def __repr__(self):
        folder = self.path.split("\\")[-1]

        date_str = self.brink_date.strftime(self.date_format)
        view = f"Deleter<{folder}\\{date_str}>"
        return view
