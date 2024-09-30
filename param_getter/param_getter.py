import os
import re
from dataclasses import dataclass, field
from datetime import date
from typing import OrderedDict
from decors import log_start
import logging
from LEXICON import DT_CODES_AND_REGEX

logger1 = logging.getLogger("main")
logger2 = logging.getLogger("duplicate_logger")


class Validations:
    def __post_init__(self):
        for name, field in self.__dataclass_fields__.items():
            method = getattr(self, f"validate_{name.lower()}", None)
            if method:
                setattr(self, name.lower(), method(getattr(self, name), field=field))


@dataclass(order=False)
class ParamScheme(Validations):
    source_folder: str
    destination_folder: str
    copy_files_or_tree: str # FILES, TREE
    schedule: str # daily,weekly,monthly,weekly_or_monthly
    save_origin: str # YES,NO
    replace_tree: str
    obsolescence_period: str # NUMBER
    substring: str # SUBSTRING
    date_format: str # YYYYMMDD, DDMMYYYY, YYYY_MM_DD, DD_MM_YYYY, YYMMDD
    date_code: str = field(init=False)
    date_regex: str = field(init=False)

    def __post_init__(self):
        date_format = self.date_format or None
        self.date_code = DT_CODES_AND_REGEX[date_format]["dt_code"]
        self.date_regex = DT_CODES_AND_REGEX[date_format]["regex"]
        if self.schedule == "weekly_or_monthly":
            if date.today().day in range(1, 6) or (
                    date.today().day in range(1, 12) and date.today().month == 1
            ):
                self.schedule = "monthly"
            else:
                self.schedule = "weekly"

    @staticmethod
    def validate_source_folder(value, **_):
        try:
            assert len(os.listdir(value)) > 0, "Неверный путь к исходной директории, или она пуста."
        except AssertionError as e:
            logger1.error("Неверный путь к исходной директории, или она пуста.", exc_info=True)
            logger2.error("Неверный путь к исходной директории, или она пуста.", exc_info=True)
            raise ValueError
        except FileNotFoundError:
            logger1.error("Исходная директория не найдена.", exc_info=True)
            logger2.error("Исходная директория не найдена.", exc_info=True)
        else:
            logger1.error(f"Исходная директория принята. {value}")
            logger2.error(f"Исходная директория принята. {value}")
        return value

    @staticmethod
    def validate_destination_folder(value, **_):
        try:
            assert len(os.listdir(value)) >= 0, "Неверный путь к директории назначения."
        except AssertionError as e:
            logger1.error("Неверный путь к директории назначения.", exc_info=True)
            logger2.error("Неверный путь к директории назначения.", exc_info=True)
            raise ValueError
        except FileNotFoundError:
            logger1.error("Директория назначения не найдена.", exc_info=True)
            logger2.error("Директория назначения не найдена.", exc_info=True)
        else:
            logger1.error(f"Директория назначения принята. {value}")
            logger2.error(f"Директория назначения принята. {value}")
        return value

    @staticmethod
    def validate_copy_files_or_tree(value, **_):
        try:
            assert value in ['FILES', 'TREE'], "COPY_FILES_OR_TREE должно иметь значение FILES или TREE."
        except AssertionError as e:
            logger1.error("COPY_FILES_OR_TREE должно иметь значение FILES или TREE.", exc_info=True)
            logger2.error("COPY_FILES_OR_TREE должно иметь значение FILES или TREE.", exc_info=True)
            raise ValueError
        return value

    @staticmethod
    def validate_schedule(value, **_):
        try:
            assert value in ["daily", "weekly", "monthly", "once"], "Неизвестное расписание. Должно быть once, daily,weekly или monthly."
        except AssertionError as e:
            logger1.error("Неизвестное расписание. Должно быть once, daily,weekly или monthly.", exc_info=True)
            logger2.error("Неизвестное расписание. Должно быть once, daily,weekly или monthly.", exc_info=True)
            raise ValueError
        return value

    @staticmethod
    def validate_save_origin(value, **_):
        try:
            assert value in ['YES', 'NO'], "Не указано сохранять ли оригинал."
        except AssertionError as e:
            logger1.error("Не указано сохранять ли оригинал.", exc_info=True)
            logger2.error("Не указано сохранять ли оригинал.", exc_info=True)
            raise ValueError
        return value

    @staticmethod
    def validate_replace_tree(value, **_):
        try:
            assert value in ['YES', 'NO'], "Не указано сохранять ли одноименные директории в папке назначения."
        except AssertionError as e:
            logger1.error("Не указано сохранять ли одноименные директории в папке назначения.", exc_info=True)
            logger2.error("Не указано сохранять ли одноименные директории в папке назначения.", exc_info=True)
            raise ValueError
        return value

    @staticmethod
    def validate_obsolescence_period(value, **_):
        try:
            assert value.isdigit() or value == "", "Период устаревания должен быть числом."
        except AssertionError as e:
            logger1.error("Период устаревания должен быть числом.", exc_info=True)
            logger2.error("Период устаревания должен быть числом.", exc_info=True)
            raise ValueError
        return value

    @staticmethod
    def validate_substring(value, **_):
        try:
            assert isinstance(value, str), "SUBSTRING должна быть строкой"
        except AssertionError as e:
            logger1.error("SUBSTRING должна быть строкой", exc_info=True)
            logger2.error("SUBSTRING должна быть строкой", exc_info=True)
            raise ValueError
        return value

    @staticmethod
    def validate_date_format(value, **_):
        try:
            assert value in ["YYYYMMDD", "DDMMYYYY", "YYYY_MM_DD", "DD_MM_YYYY", "YYMMDD", ''], "Установите формат даты: YYYYMMDD, DDMMYYYY, YYYY_MM_DD, DD_MM_YYYY, YYMMDD."
        except AssertionError as e:
            logger1.error("Установите формат даты: YYYYMMDD, DDMMYYYY, YYYY_MM_DD, DD_MM_YYYY, YYMMDD.", exc_info=True)
            logger2.error("Установите формат даты: YYYYMMDD, DDMMYYYY, YYYY_MM_DD, DD_MM_YYYY, YYMMDD.", exc_info=True)
            raise ValueError
        return value




class ParamGetter:
    def __init__(self, env_variables: OrderedDict[str, str]):
        self.vars = env_variables
        self.as_dct = self.get_param_groups()
        self.as_schemes = self.get_param_schemes()

    @staticmethod
    def check_group(dct):
        """Проверка одной группы параметров"""
        flag = True
        ParamScheme(**dct)
        if len(dct) != 9:
            flag = False

        # for k, v in dct.items():
        #     print(k,v)
        #     if not k or not v:
        #         flag = False

        if flag:
            return True

        raise NameError("Переменные env некорректны.")

    @log_start
    def get_param_groups(self):
        """Прием групп параметров из файла env"""
        regex = r"^(.+)_(\d+)$"
        param_groups = {}

        for var, value in self.vars.items():
            match = re.fullmatch(regex, var)
            if match.group(2).isdigit():
                id_num = int(match.group(2))
                dct = param_groups.setdefault(id_num, {})
                dct[match.group(1).lower()] = value

        #
        # for gr in param_groups.values():
        #     self.check_group(gr)

        return param_groups

    def get_param_schemes(self):
        dct = {}
        for i, v in self.as_dct.items():

            dct[i] = ParamScheme(**v)
        return dct



    def __str__(self):
        lst = []
        for var, val in self.vars.items():
            if "SOURCE" in var:
                lst.append(val)
        view = f"ParamGetter<{lst}>"
        return view

    def __repr__(self):
        lst = []
        for var, val in self.vars.items():
            if "SOURCE" in var:
                lst.append(val)
        view = f"ParamGetter<{lst}>"
        return view
