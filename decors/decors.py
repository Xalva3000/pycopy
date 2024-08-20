"""Декораторы функций"""
import logging
from functools import wraps
from time import perf_counter


def timer(func):
    """Декоратор замера времени работы функции"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger1 = logging.getLogger("main")
        logger2 = logging.getLogger("duplicate_logger")
        func_doc = func.__doc__
        start = perf_counter()
        result = func(*args, **kwargs)
        stop = (perf_counter() - start).__round__(2)
        logger1.info(f"Задача '{func_doc}' завершена за {stop}.\n")
        logger2.info(f"Задача '{func_doc}' завершена за {stop}.\n")
        return result
    return wrapper


def log_start_finish(func):
    """Декоратор логирования сообщает о запуске и завершении работы функции"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger1 = logging.getLogger("main")
        logger2 = logging.getLogger("duplicate_logger")
        func_doc = func.__doc__
        logger1.info(f"Задача '{func_doc}' запускается. Параметры {args}")
        logger2.info(f"Задача '{func_doc}' запускается. Параметры {args}")
        result = func(*args, **kwargs)
        logger1.info(f"Задача завершена, '{func_doc}'")
        logger2.info(f"Задача завершена, '{func_doc}'")
        return result
    return wrapper


def log_finish(func):
    """Декоратор логирования сообщает о завершении функции"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger1 = logging.getLogger("main")
        logger2 = logging.getLogger("duplicate_logger")
        func_doc = func.__doc__
        result = func(*args, **kwargs)
        logger1.info(f"Успешно: '{func_doc}'. Параметры: {args}")
        logger2.info(f"Успешно: '{func_doc}'. Параметры: {args}")
        return result
    return wrapper


def log_start(func):
    """Декоратор логирования сообщает о запуске функции"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger1 = logging.getLogger("main")
        logger2 = logging.getLogger("duplicate_logger")
        func_doc = func.__doc__
        logger1.info(f"Запуск: '{func_doc}'. Параметры: {args}\n")
        logger2.info(f"Запуск: '{func_doc}'. Параметры: {args}\n")
        result = func(*args, **kwargs)
        return result
    return wrapper


