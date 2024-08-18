from random import randint

from LEXICON import NEW_ENV_FILE
from decors import timer


@timer
def filler(path):
    """Функция заполнения файлов для ручного
    и автоматического тестирования
    до объема в ~50Мб"""
    with open(path, 'w', encoding="utf-8") as file:
        for _ in range(10_000_000):
            file.write(f"{randint(10000, 1000000)}")


def create_big_files(path, amount):
    """Создание и заполнение тестовых фалов, примерно по 50Мб,
    занимает время. (для ручного тестирования и
    визуального осмотра работы программы)"""
    for file in [f'{i}.txt' for i in range(1, amount+1)]:
        filler(path + file)


def create_readme_file(mess):
    """Создание файла README.txt"""
    with open(f'README.txt', "w", encoding='utf-8') as file:
        file.write(mess)


def create_env_file():
    """Создание и заполнение файла env."""
    with open(".env", "w", encoding="utf-8") as file:
        file.write(NEW_ENV_FILE)
