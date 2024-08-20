import os
import re
from datetime import datetime, date, timedelta


class Searcher:
    """Класс для определения списка копируемых файлов"""

    def __init__(self, source_path, destination_path, mode="FILES", trigger=None):
        if mode == "FILES":
            self.source = list(
                filter(
                    lambda name: os.path.isfile(
                        os.path.join(source_path, name)),
                        os.listdir(source_path)))
            self.destination = list(
                filter(
                    lambda name: os.path.isfile(
                        os.path.join(destination_path, name)),
                        os.listdir(destination_path)))
        elif mode == "TREE":
            self.source = list(
                filter(
                    lambda name: os.path.isdir(
                        os.path.join(source_path, name)),
                        os.listdir(source_path)))
            self.destination = list(
                filter(
                    lambda name: os.path.isdir(
                        os.path.join(destination_path, name)),
                        os.listdir(destination_path)))

        if trigger == "YYYYMMDD":
            self.regex = r"(\d{8})"
            self.repr_format = "%Y%m%d"
        elif trigger == "YYMMDD":
            self.regex = r"(\d{6})"
            self.repr_format = "%y%m%d"
        elif trigger == "DD_MM_YYYY":
            self.regex = r"(\d\d_\d\d_\d{4})"
            self.repr_format = "%d_%m_%Y"
        elif trigger == "YYYY_MM_DD":
            self.regex = r"(\d{4}_\d\d_\d\d)"
            self.repr_format = "%Y_%m_%d"
        else:
            self.trigger = trigger



    def _latest_date(self, lst):
        dates = []
        for file_name in lst:
            match = re.search(self.regex, file_name)
            if match and match.group(1):
                dates.append(datetime.strptime(match.group(1), self.repr_format))
        if dates:
            latest_date = max(dates)
            return latest_date
        return None

    def _dated_files(self, lst):
        dated_files = list(filter(lambda d: re.search(self.regex, d), lst))
        return dated_files

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
                file_date = datetime.strptime(match.group(1), self.repr_format).date()
                if file_date > oldest_date:
                    actual_source.append(name)

        actual_difference = set(self.source).difference(self.destination)
        return actual_difference


    def get_latest_difference(self):
        latest_date_source = self._latest_date(self.source)
        latest_date_destination = self._latest_date(self.destination)
        latest_source = []

        if not latest_date_destination or latest_date_source > latest_date_destination:
            for name in self.source:
                if latest_date_source.strftime(self.repr_format) in name:
                    latest_source.append(name)
        latest_difference = set(latest_source).difference(self.destination)
        return latest_difference

    def get_triggered_names(self, difference=False):
        triggered_names = filter(lambda name: self.trigger in name, self.source)
        if not difference:
            return set(triggered_names)
        else:
            return set(triggered_names).difference(self.destination)







