LEXICON_RU = {
    "new_env_message": """Создан файл .env.\n Заполните его как указано в README.txt""",
    "new_env_file": """Создан файл .env.\n\n
    Заполните его с помощью тестового редактора 
    относительно каждой копируемой директории.\n\n\n
    SOURCE_FOLDER_1 - путь к первой исходной папке.\n
    DESTINATION_FOLDER_1 - путь к первой папке назначения.\n
    SCHEDULE_1 - список первого режима расписания (daily,weekly,monthly).\n
    SAVE_ORIGIN_1 - первый режим удаления (YES или NO).\n
    OBSOLESCENCE_PERIOD_1=7 - для ежедневного копирования указать период
        в днях, после которого файл считается устаревшим).\n
    DATE_FORMAT_1=YYYYMMDD - формат даты. (Поддерживается: 20240816,
        2024_08_16, 16_08_2024)\n\n\n""",
}

NEW_ENV_FILE = """SOURCE_FOLDER_1=
DESTINATION_FOLDER_1=
SCHEDULE_1=daily,weekly,monthly
SAVE_ORIGIN_1=NO
OBSOLESCENCE_PERIOD_1=7
DATE_FORMAT_1=YYYYMMDD"""