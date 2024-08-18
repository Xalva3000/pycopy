import os
import re
from datetime import datetime, date, timedelta


class Searcher:
    """Класс для определения списка копируемых файлов"""

    def __init__(self, source_path, destination_path, date_format):
        self.source_path = source_path
        self.destination_path = destination_path

        if date_format == "YYYYMMDD":
            self.regex = r"^(\d{8})_.+"
            self.repr_date = "%Y%m%d"
        elif date_format == "DD_MM_YYYY":
            self.regex = r"^(\d\d_\d\d_\d{4})_.+"
            self.repr_date = "%d_%m_%Y"
        elif date_format == "YYYY_MM_DD":
            self.regex = r"^(\d{4}_\d\d_\d\d)_.+"
            self.repr_date = "%Y_%m_%d"

    def _latest_date(self, lst):
        dates = []
        for file_name in lst:
            match = re.fullmatch(self.regex, file_name)
            if match and match.group(1):
                dates.append(datetime.strptime(match.group(1), self.repr_date))
        latest_date = max(dates)
        return latest_date

    def _dated_files(self, lst):
        dated_files = list(filter(lambda d: re.fullmatch(self.regex, d), lst))
        return dated_files

    def get_full_difference(self):
        """Возвращает массив названий файлов, содержащихся
        в исходной папке, которых нет в папке назначения"""
        source = os.listdir(self.source_path)
        destination = os.listdir(self.destination_path)
        result = set(source).difference(destination)
        return result


    def get_actual_difference(self, period: int = 7):
        source = os.listdir(self.source_path)
        destination = os.listdir(self.destination_path)
        oldest_date = datetime.today() - timedelta(days=period) 



    def get_latest_difference(self):
        source = os.listdir(self.source_path)
        destination = os.listdir(self.destination_path)



