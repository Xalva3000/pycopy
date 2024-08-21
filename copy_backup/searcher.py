import os
import re
from datetime import datetime, date, timedelta


class Searcher:
    """Класс для определения списка копируемых файлов"""
    DT_FORMATS = {"YYYYMMDD": {"regex": r"(\d{8})", "dt_code": "%Y%m%d"},
                  "YYMMDD": {"regex": r"(\d{6})", "dt_code": "%y%m%d"},
                  "DD_MM_YYYY": {"regex": r"(\d\d_\d\d_\d{4})", "dt_code": "%d_%m_%Y"},
                  "YYYY_MM_DD": {"regex": r"(\d{4}_\d\d_\d\d)", "dt_code": "%Y_%m_%d"},
                  None: {"regex": "", "dt_code": ""}}

    def __init__(self, source_path, destination_path, mode="FILES", substring=None, dt_format=None):
        self.mode = mode
        self.dt_format = dt_format
        self.regex = Searcher.DT_FORMATS[dt_format]["regex"]
        self.date_format = Searcher.DT_FORMATS[dt_format]["dt_code"]
        self.substring = substring or ""
        self.source = self.accept_filters(source_path)
        self.destination = self.accept_filters(destination_path)


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
            return list(filter(lambda name: re.search(regex, name), lst))
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
            match = re.search(self.regex, file_name)
            if match and match.group(1):
                dates.append(datetime.strptime(match.group(1), self.date_format))
        if dates:
            latest_date = max(dates)
            return latest_date
        return None

    def get_full_difference(self):
        """Возвращает массив названий файлов, содержащихся
        в исходной папке, которых нет в папке назначения"""
        full_difference = set(self.source).difference(self.destination)
        return full_difference


    def get_actual_difference(self, period: int = 7):
        """Возвращает массив названий актуальных (неустаревших) файлов,
        из исходной попки, которых нет в папке назначения"""
        oldest_date = (datetime.today() - timedelta(days=period)).date()
        actual_source = []

        for name in self.source:
            match = re.search(self.regex, name)
            if match:
                file_date = datetime.strptime(match.group(1), self.date_format).date()
                if file_date > oldest_date:
                    actual_source.append(name)

        actual_difference = set(self.source).difference(self.destination)
        return actual_difference

    def get_latest(self, lst):
        latest_date_str = self._latest_date(lst).strftime(self.date_format)
        result = list(filter(lambda name: latest_date_str in name, lst))
        return result


    def get_latest_difference(self):
        latest_date_source = self._latest_date(self.source)
        latest_date_destination = self._latest_date(self.destination)
        latest_source = []

        if not latest_date_destination or latest_date_source > latest_date_destination:
            for name in self.source:
                if latest_date_source.strftime(self.date_format) in name:
                    latest_source.append(name)
        latest_difference = set(latest_source).difference(self.destination)
        return latest_difference
