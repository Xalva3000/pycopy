import dotenv
from datetime import date
import os


dotenv.load_dotenv()

# Создание и заполнение тестовых файлов c датами (для ручного тестирования)
def make_fake_files():
    # os.makedirs(r"C:\set1", exist_ok=True)
    # os.makedirs(r"C:\set2", exist_ok=True)
    # os.makedirs(r"C:\set3", exist_ok=True)
    # os.makedirs(r"C:\set4", exist_ok=True)

    for k, v in dotenv.dotenv_values().items():
        if 'SOURCE_FOLDER' in k:
            os.makedirs(v, exist_ok=True)
            source = v


            today_ordinal = date.today().toordinal()
            month_before = today_ordinal - 30
            for i in range(month_before, today_ordinal + 1):
                name = f'file_{date.fromordinal(i).strftime("%y%m%d")}.txt'
                with open(source + name, "w", encoding="utf-8") as f_in:
                    f_in.write(name)

                new_folder = source + f'folder_{date.fromordinal(i).strftime("%y%m%d")}'
                os.makedirs(new_folder, exist_ok=True)

                for i in range(month_before, today_ordinal + 1):
                    name = new_folder + "\\" + f'{date.fromordinal(i).strftime("%y%m%d")}_file.txt'
                    with open(name, "w", encoding="utf-8") as f_in:
                        f_in.write(name)

            for i in range(month_before, today_ordinal + 1):
                name = f'{date.fromordinal(i).strftime("%y%m%d")}_file.txt'
                with open(source + name, "w", encoding="utf-8") as f_in:
                    f_in.write(name)

                new_folder = source + f'{date.fromordinal(i).strftime("%y%m%d")}_folder'
                os.makedirs(new_folder, exist_ok=True)

            for i in range(month_before, today_ordinal + 1):
                name = f'{date.fromordinal(i).strftime("%Y%m%d")}_file.txt'
                with open(source + name, "w", encoding="utf-8") as f_in:
                    f_in.write(name)

                new_folder = source + f'{date.fromordinal(i).strftime("%Y%m%d")}_folder'
                os.makedirs(new_folder, exist_ok=True)

            for i in range(month_before, today_ordinal + 1):
                name = f'file_{date.fromordinal(i).strftime("%Y%m%d")}.txt'
                with open(source + name, "w", encoding="utf-8") as f_in:
                    f_in.write(name)

                new_folder = source + f'folder_{date.fromordinal(i).strftime("%Y%m%d")}'
                os.makedirs(new_folder, exist_ok=True)

        if 'DESTINATION_FOLDER' in k:
            os.makedirs(v, exist_ok=True)


if __name__ == "__main__":
    make_fake_files()
