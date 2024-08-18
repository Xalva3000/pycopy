import os
import re
from datetime import datetime, date, timedelta


class Searcher:
    """Класс для определения списка копируемых файлов"""

    def __init__(self, source_path, destination_path, date_format):
        self.source_path = source_path
        self.destination_path = destination_path

        if date_format == "YYYYMMDD":
            self.regex = r"(\d{8})"
            self.repr_format = "%Y%m%d"
        elif date_format == "DD_MM_YYYY":
            self.regex = r"(\d\d_\d\d_\d{4})"
            self.repr_format = "%d_%m_%Y"
        elif date_format == "YYYY_MM_DD":
            self.regex = r"(\d{4}_\d\d_\d\d)"
            self.repr_format = "%Y_%m_%d"

    def _latest_date(self, lst):
        dates = []
        for file_name in lst:
            match = re.search(self.regex, file_name)
            if match and match.group(1):
                dates.append(datetime.strptime(match.group(1), self.repr_format))
        latest_date = max(dates)
        return latest_date

    def _dated_files(self, lst):
        dated_files = list(filter(lambda d: re.search(self.regex, d), lst))
        return dated_files

    def get_full_difference(self):
        """Возвращает массив названий файлов, содержащихся
        в исходной папке, которых нет в папке назначения"""
        source = os.listdir(self.source_path)
        destination = os.listdir(self.destination_path)
        full_difference = set(source).difference(destination)
        return full_difference


    def get_actual_difference(self, period: int = 7):
        """Возвращает массив названий актуальных (неустаревших) файлов,
        из исходной попки, которых нет в папке назначения"""
        source = os.listdir(self.source_path)
        destination = os.listdir(self.destination_path)
        oldest_date = (datetime.today() - timedelta(days=period)).date()
        actual_source = []

        for name in source:
            match = re.search(self.regex, name)
            if match:
                file_date = datetime.strptime(match.group(1), self.repr_format).date()
                if file_date > oldest_date:
                    actual_source.append(name)

        actual_difference = set(source).difference(destination)
        return actual_difference


    def get_latest_difference(self):
        source = os.listdir(self.source_path)
        destination = os.listdir(self.destination_path)
        latest_date = self._latest_date(source)
        latest_source = []

        for name in source:
            if latest_date.strftime(self.repr_format) in name:
                latest_source.append(name)

        latest_difference = set(latest_source).difference(destination)
        return latest_difference




