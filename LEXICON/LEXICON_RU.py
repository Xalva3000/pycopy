LEXICON_RU = {
    "new_env_message": """Создан файл .env.\n Заполните его как указано в README.txt""",
    "new_env_file": """Создан файл .env.\n\n
    Заполните его с помощью текстового редактора 
    относительно каждой копируемой директории.\n\n\n
    SOURCE_FOLDER_1=C:\\test1\\ - путь к первой исходной папке.\n
    DESTINATION_FOLDER_1=C:\\test2\\ - путь к первой папке назначения.\n
    COPY_FILES_OR_FOLDERS_1=FILES - режим копирования файлов или папки целиком\n
    SCHEDULE_1=weekly,monthly - список первого режима расписания (daily,weekly,monthly).\n
    SAVE_ORIGIN_1=YES - сохранять ли оригинал (YES или NO).\n
    OBSOLESCENCE_PERIOD_1=7 - для ежедневного копирования указать период
        в днях, после которого файл считается устаревшим).\n
    TRIGGER_1=YYYYMMDD - подстрока, имя или формат даты. (Поддерживается: 20240816=YYYYMMDD,
        2024_08_16=YYYY_MM_DD, 16_08_2024=DD_MM_YYYY)\n\n\n

Пример для второй папке

SOURCE_FOLDER_2=C:\\test3\\ - путь к второй исходной папке.
DESTINATION_FOLDER_2=C:\\test4\\ - путь к второй папке назначения.
COPY_FILES_OR_FOLDERS_2=FILES
SCHEDULE_2=daily
SAVE_ORIGIN_2=YES
OBSOLESCENCE_PERIOD_2=7
TRIGGER_2=YYYYMMDD\n

Важные моменты:
-Все поля обязательны к заполнению, даже если они не используются.
Расписание можно указывать списком, например сразу: daily,weekly,monthly 
-или одиночное: daily
-Для daily важно указывать период устаревания. Удаление осуществляется
по этой цифре, обязательно, не учитывая поле "сохранение оригинала".
-Расписания monthly и weekly копируют один, самый новый по дате файл,
и его удаляют, если указано "не сохранять оригинал".
-Расписание monthly и weekly запускаются только в случае
более новой даты исходного файла, чем у файлов в папке назначения.
""",
}

NEW_ENV_FILE = """SOURCE_FOLDER_1=
DESTINATION_FOLDER_1=
COPY_FILES_OR_FOLDERS_1=FILES
SCHEDULE_1=weekly,monthly
SAVE_ORIGIN_1=YES
OBSOLESCENCE_PERIOD_1=7
TRIGGER_1=YYYYMMDD

SOURCE_FOLDER_2=
DESTINATION_FOLDER_2=
COPY_FILES_OR_FOLDERS_2=FILES
SCHEDULE_2=daily
SAVE_ORIGIN_2=YES
OBSOLESCENCE_PERIOD_2=7
TRIGGER_2=YYYYMMDD
"""

SUPPORTED_DATE_FORMATS = ("YYYYMMDD", "DDMMYYYY", "YYYY_MM_DD", "DD_MM_YYYY", "YYMMDD")
