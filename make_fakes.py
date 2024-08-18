import dotenv
from datetime import date


dotenv.load_dotenv()

# Создание и заполнение тестовых файлов c датами (для ручного тестирования)
def make_fake_files():

    for k, v in dotenv.dotenv_values().items():
        if 'SOURCE_FOLDER' in k:

            source = v


        today_ordinal = date.today().toordinal()
        month_before = today_ordinal - 30
        for i in range(month_before, today_ordinal + 1):
            name = f'{date.fromordinal(i).strftime("%Y%m%d")}_file.txt'
            with open(source + name, "w", encoding="utf-8") as f_in:
                f_in.write(name)

if __name__ == "__main__":
    make_fake_files()