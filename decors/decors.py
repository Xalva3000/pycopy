"""Декораторы функций"""
import logging
from functools import wraps
from time import perf_counter


def timer(func):
    """Декоратор замера времени работы функции"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger("main")
        func_doc = func.__doc__
        start = perf_counter()
        result = func(*args, **kwargs)
        stop = (perf_counter() - start).__round__(2)
        logger.info(f"Задача '{func_doc}' завершена за {stop}.\n")
        return result
    return wrapper


def log_start_finish(func):
    """Декоратор логирования сообщает о запуске и завершении работы функции"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger("main")
        func_doc = func.__doc__
        logger.info(f"Задача '{func_doc}' запускается. Параметры {args}")
        result = func(*args, **kwargs)
        logger.info(f"Задача завершена, '{func_doc}'")
        return result
    return wrapper


def log_finish(func):
    """Декоратор логирования сообщает о завершении функции"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger("main")
        func_doc = func.__doc__
        result = func(*args, **kwargs)
        logger.info(f"Успешно: '{func_doc}'. Параметры: {args}")
        return result
    return wrapper


def log_start(func):
    """Декоратор логирования сообщает о запуске функции"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger("main")
        func_doc = func.__doc__
        logger.info(f"Запуск: '{func_doc}'. Параметры: {args}")
        result = func(*args, **kwargs)
        return result
    return wrapper


