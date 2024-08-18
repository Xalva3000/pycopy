import logging
import os
import re
from dataclasses import dataclass
from typing import OrderedDict
from decors import log_finish
import logging


logger = logging.getLogger(__name__)


class Validations:
    def __post_init__(self):
        for name, field in self.__dataclass_fields__.items():
            method = getattr(self, f"validate_{name}", None)
            if method:
                setattr(self, name, method(getattr(self, name), field=field))


@dataclass
class ParamScheme(Validations):
    SOURCE_FOLDER: str
    DESTINATION_FOLDER: str
    SCHEDULE: str
    SAVE_ORIGIN: str
    OBSOLESCENCE_PERIOD: int

    @staticmethod
    def validate_SOURCE_FOLDER(value, **_):
        try:
            assert len(os.listdir(value)) > 0,"Неверный путь к исходной папке, или она пуста."
        except Exception as e:
            logger.error("Неверный путь к исходной папке, или она пуста.", exc_info=True)

    @staticmethod
    def validate_DESTINATION_FOLDER(value, **_):
        try:
            assert len(os.listdir(value)) >= 0, "Неверный путь к папке назначения."
        except Exception as e:
            logger.error("Неверный путь к папке назначения.", exc_info=True)

    # @staticmethod
    # def validate_SCHEDULE(value, **_):
    #     try:
    #         assert value in ['daily', 'w/m'], "Неизвестное расписание."
    #     except Exception as e:
    #         logger.error("Неизвестное расписание.", exc_info=True)

    @staticmethod
    def validate_SAVE_ORIGIN(value, **_):
        try:
            assert value in ['YES', 'NO'], "Не указано сохранять ли оригинал."
        except Exception as e:
            logger.error("Не указано сохранять ли оригинал.", exc_info=True)

    @staticmethod
    def validate_OBSOLESCENCE_PERIOD(value, **_):
        try:
            assert value.isdigit(), "Период устаревания должен быть числом."
        except Exception as e:
            logger.error("Период устаревания должен быть числом.", exc_info=True)


class ParamGetter:
    def __init__(self, env_variables: OrderedDict[str, str]):
        self.vars = env_variables

    def check_raw(self):
        if len(self.vars) % 5 == 0:
            return True
        return

    @staticmethod
    def check_groups(dct):
        """Проверка одной группы параметров"""
        flag = True
        ParamScheme(**dct)
        if len(dct) != 5:
            flag = False

        for k, v in dct.items():
            if not k or not v:
                flag = False

        if flag:
            return True

        raise NameError("Переменные env некорректны.")

    @log_finish
    def get_param_groups(self):
        """Прием групп параметров из файла env"""
        regex = r"^(.+)_(\d+)$"
        param_groups = {}

        for var, value in self.vars.items():
            match = re.fullmatch(regex, var)
            if match.group(2).isdigit():
                id_num = int(match.group(2))
                dct = param_groups.setdefault(id_num, {})
                dct[match.group(1)] = value

        for gr in param_groups.values():
            self.check_groups(gr)

        return param_groups

    def __str__(self):
        lst = []
        for var in self.vars:
            if "SOURCE" in var:
                lst.append(var)
        view = f"ParamGetter<{lst}>"
        return view

    def __repr__(self):
        lst = []
        for var, val in self.vars.items():
            if "SOURCE" in var:
                lst.append(val)
        view = f"ParamGetter<{lst}>"
        return view


