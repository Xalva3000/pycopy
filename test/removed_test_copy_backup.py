import unittest
from datetime import date

from copy_backup import CopyBackup
from filler.filler import filler
import os
import shutil


class TestCopyBackup(unittest.TestCase):
    def setUp(self):
        self.PATH_SOURCE = r'in-files'
        self.PATH_DESTINATION = r'out_files'
        os.mkdir(self.PATH_SOURCE)
        os.mkdir(self.PATH_DESTINATION)
        self.files = [f'small_file_{i}.txt' for i in range(1,11)]


    def test_copyobj(self):
        for file in self.files:
            with open(self.PATH_SOURCE + '\\' + file, 'w', encoding='utf-8') as f:
                f.write(file)
        copy_backup = CopyBackup(self.PATH_SOURCE + '\\', self.PATH_DESTINATION + '\\', self.files)
        copy_backup.copy_obj_all()
        directory = os.listdir(self.PATH_DESTINATION)

        for file in self.files:
            self.assertIn(copy_backup.dated_name(file), directory)

            self.assertEqual(
                os.path.getsize(self.PATH_SOURCE + '\\' + file),
                os.path.getsize(self.PATH_DESTINATION + '\\' + CopyBackup.dated_name(file))
            )

    def test_copyobj_big_files(self):
        big_files = ['big_file.txt', 'big_file.txt']
        for file in big_files:
            filler(self.PATH_SOURCE + '\\' + file)

        copy_backup = CopyBackup(self.PATH_SOURCE + '\\', self.PATH_DESTINATION + '\\', big_files)
        copy_backup.copy_obj_all()
        directory = os.listdir(self.PATH_DESTINATION)

        for file in big_files:
            self.assertIn(copy_backup.dated_name(file), directory)

            self.assertEqual(
                os.path.getsize(self.PATH_SOURCE + '\\' + file),
                os.path.getsize(self.PATH_DESTINATION + '\\' + copy_backup.dated_name(file))
            )

    def test_load_by_quantity(self):
        files = [f'small_file_{i}.txt' for i in range(1,1001)]
        self.assertEqual(len(files), 1000)
        for file in files:
            with open(self.PATH_SOURCE + '\\' + file, 'w', encoding='utf-8') as f:
                f.write(file)
        copy_backup = CopyBackup(self.PATH_SOURCE + '\\', self.PATH_DESTINATION + '\\', files)
        copy_backup.copy_obj_all()
        directory = os.listdir(self.PATH_DESTINATION)

        for file in files:
            self.assertIn(copy_backup.dated_name(file), directory)

            self.assertEqual(
                os.path.getsize(self.PATH_SOURCE + '\\' + file),
                os.path.getsize(self.PATH_DESTINATION + '\\' + CopyBackup.dated_name(file))
            )

    def test_copy_subproc(self):
        for file in self.files:
            with open(self.PATH_SOURCE + '\\' + file, 'w', encoding='utf-8') as f:
                f.write(file)
        copy_backup = CopyBackup(self.PATH_SOURCE + '\\', self.PATH_DESTINATION + '\\', self.files)
        copy_backup.copy_subproc_all()
        directory = os.listdir(self.PATH_DESTINATION)

        for file in self.files:
            self.assertIn(copy_backup.dated_name(file), directory)

            self.assertEqual(
                os.path.getsize(self.PATH_SOURCE + '\\' + file),
                os.path.getsize(self.PATH_DESTINATION + '\\' + CopyBackup.dated_name(file))
            )

    def test_copy_subproc_big_files(self):
        big_files = ['big_file.txt', 'big_file.txt']
        for file in big_files:
            filler(self.PATH_SOURCE + '\\' + file)

        copy_backup = CopyBackup(self.PATH_SOURCE + '\\', self.PATH_DESTINATION + '\\', big_files)
        copy_backup.copy_subproc_all()
        directory = os.listdir(self.PATH_DESTINATION)

        for file in big_files:
            self.assertIn(copy_backup.dated_name(file), directory)

            self.assertEqual(
                os.path.getsize(self.PATH_SOURCE + '\\' + file),
                os.path.getsize(self.PATH_DESTINATION + '\\' + copy_backup.dated_name(file))
            )

    def test_subproc_load_by_quantity(self):
        files = [f'small_file_{i}.txt' for i in range(1,1001)]
        self.assertEqual(len(files), 1000)
        for file in files:
            with open(self.PATH_SOURCE + '\\' + file, 'w', encoding='utf-8') as f:
                f.write(file)
        copy_backup = CopyBackup(self.PATH_SOURCE + '\\', self.PATH_DESTINATION + '\\', files)
        copy_backup.copy_subproc_all()
        directory = os.listdir(self.PATH_DESTINATION)

        for file in files:
            self.assertIn(copy_backup.dated_name(file), directory)

            self.assertEqual(
                os.path.getsize(self.PATH_SOURCE + '\\' + file),
                os.path.getsize(self.PATH_DESTINATION + '\\' + CopyBackup.dated_name(file))
            )


    def tearDown(self):
        shutil.rmtree(self.PATH_SOURCE)
        shutil.rmtree(self.PATH_DESTINATION)


if __name__ == "__main__":
    unittest.main()