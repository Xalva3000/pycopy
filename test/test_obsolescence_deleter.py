def branch():
    SOURCE_FOLDER = os.getenv('SOURCE_FOLDER')
    DESTINATION_FOLDER = os.getenv('DESTINATION_FOLDER')

    today_ordinal = date.today().toordinal()
    month_before = today_ordinal - 30

    for i in range(month_before, today_ordinal + 1):
        name = f'{date.fromordinal(i).strftime("%y%m%d")}_file.txt'
        with open(SOURCE_FOLDER + name, 'w', encoding='utf-8') as f_in:
            f_in.write(name)

    copy_backup = CopyBackup(SOURCE_FOLDER, DESTINATION_FOLDER)

    deleter_in = ObsolescenceDeleter(SOURCE_FOLDER, 7)
    deleter_out = ObsolescenceDeleter(DESTINATION_FOLDER, 7)

    copy_backup.copy_obj_all()


    if copy_backup.check_size():
        deleter_in.delete_outdated()
        deleter_out.delete_outdated()