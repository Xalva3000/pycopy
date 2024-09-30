import os
import re
from datetime import datetime, date, timedelta
from param_getter import ParamScheme
import logging


logger = logging.getLogger("main")


class Searcher:
    """Класс для определения списка копируемых файлов"""
    def __init__(self, destination_path, params: ParamScheme):
        self.params = params
        self.mode = params.copy_files_or_tree
        self.dt_format = params.date_format or None
        self.regex = self.params.date_regex
        self.date_format = self.params.date_code
        self.substring = self.params.substring
        self.source = self.accept_filters(params.source_folder)
        self.destination = self.accept_filters(destination_path)

        if params.schedule == "daily":
            if self.params.date_format:
                self.files = self.get_actual_difference()
            else:
                self.files = self.get_full_difference()

        elif params.schedule == "weekly" or params.schedule == "monthly":
            if self.params.date_format:
                self.files = self.get_latest()
            else:
                self.files = self.get_full_difference()
        elif params.schedule == "once":
            if self.params.date_format:
                self.files = self.get_latest()
            else:
                self.files = self.get_full_difference()

    @staticmethod
    def _filter_mode(path, mode):
        if mode == "FILES":
            lst = list(
                filter(
                    lambda name: os.path.isfile(
                        os.path.join(path, name)),
                    os.listdir(path)))
        elif mode == "TREE":
            lst = list(
                filter(
                    lambda name: os.path.isdir(
                        os.path.join(path, name)),
                        os.listdir(path)))
        else:
            lst = []
        return lst

    @staticmethod
    def _filter_substring(lst, substring):
        if substring:
            return list(filter(lambda name: substring in name, lst))
        return lst

    @staticmethod
    def _filter_date_format(lst, regex):
        if regex:
            return list(filter(lambda name: re.search(regex, name.split(".")[0]), lst))
        return lst

    def accept_filters(self, path):
        lst = self._filter_mode(path, self.mode)
        if self.substring:
            lst = self._filter_substring(lst, self.substring)
        if self.dt_format:
            lst = self._filter_date_format(lst, self.regex)
        return lst

    def _latest_date(self, lst):
        dates = []
        for file_name in lst:
            match = re.search(self.regex, file_name.split(".")[0])

            if match:
                gr = match.group(1) or match.group(2)
                dates.append(datetime.strptime(gr, self.date_format))
        if dates:
            latest_date = max(dates)
            return latest_date
        return None

    def get_full_difference(self):
        """Возвращает массив названий файлов, содержащихся
        в исходной папке, которых нет в папке назначения"""
        logger.info("Выбор отсутствующих в директории назначения объектов.")
        full_difference = set(self.source).difference(self.destination)
        return full_difference

    def get_actual_difference(self):
        """Возвращает массив названий актуальных (неустаревших) файлов,
        из исходной попки, которых нет в папке назначения"""
        logger.info(f"Выбор актуальных по дате объектов. Период устаревания {self.params.obsolescence_period} дней.")
        oldest_date = (datetime.today() - timedelta(days=int(self.params.obsolescence_period))).date()
        actual_source = []
        for name in self.source:
            match = re.search(self.regex, name.split(".")[0])
            if match:
                _dt = match.group(1) or match.group(2)
                file_date = datetime.strptime(_dt, self.date_format).date()
                if file_date > oldest_date:
                    actual_source.append(name)

        actual_difference = set(actual_source).difference(self.destination)
        return actual_difference

    def get_latest(self, lst=None):
        logger.info("Выбор самых ближних по дате объектов.")
        _lst = lst or self.source
        if self.date_format and _lst:
            latest_date_str = self._latest_date(_lst).strftime(self.date_format)
            result = list(filter(lambda name: latest_date_str in name, _lst))
            return result
        return _lst

    def get_latest_difference(self):
        logger.info("Выбор ближних по дате объектов, отсутствующих в директории назначения.")
        latest_date_source = self._latest_date(self.source)
        latest_date_destination = self._latest_date(self.destination)
        latest_source = []
        if not latest_date_destination or latest_date_source > latest_date_destination:
            for name in self.source:
                if latest_date_source.strftime(self.date_format) in name:
                    latest_source.append(name)
        latest_difference = set(latest_source).difference(self.destination)
        return latest_difference
