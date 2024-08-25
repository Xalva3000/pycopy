from time import sleep

import dotenv
from tqdm import tqdm

from LEXICON import LEXICON_RU
from param_getter import ParamGetter
import os
from sys import exit

from filler import create_env_file, create_readme_file

if ".env" not in os.listdir("."):

    mess = LEXICON_RU["new_env_message"]
    create_env_file()
    create_readme_file(LEXICON_RU["new_env_file"])
    print(mess)
    for i in tqdm(range(10)):
        sleep(1)
    exit()

# Загрузка переменных из файла .env,
# в котором пользователь указывает пути и список файлов,
# в окружение
dotenv.load_dotenv()
param_getter = ParamGetter(dotenv.dotenv_values())

# Объявление переменных из окружения
# SOURCE_FOLDER = os.getenv('SOURCE_FOLDER')
# DESTINATION_FOLDER = os.getenv('DESTINATION_FOLDER')
# MODE = os.getenv('MODE')

