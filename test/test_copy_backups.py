import unittest
from datetime import date
from random import randint

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
        copy_backup = CopyBackup(self.PATH_SOURCE + '\\', self.PATH_DESTINATION + '\\')
        copy_backup.copy_obj_all()
        directory = os.listdir(self.PATH_DESTINATION)

        for file in self.files:
            self.assertIn(file, directory)

            self.assertEqual(
                os.path.getsize(self.PATH_SOURCE + '\\' + file),
                os.path.getsize(self.PATH_DESTINATION + '\\' + file)
            )

    def test_copyobj_big_files(self):
        big_files = ['big_file1.txt', 'big_file2.txt']
        for file in big_files:
            filler(self.PATH_SOURCE + '\\' + file)

        copy_backup = CopyBackup(self.PATH_SOURCE + '\\', self.PATH_DESTINATION + '\\')
        copy_backup.copy_obj_all()
        directory = os.listdir(self.PATH_DESTINATION)

        for file in big_files:
            self.assertIn(file, directory)

            self.assertEqual(
                os.path.getsize(self.PATH_SOURCE + '\\' + file),
                os.path.getsize(self.PATH_DESTINATION + '\\' + file)
            )

    def test_load_by_quantity(self):
        files = [f'small_file_{i}.txt' for i in range(1,1001)]
        self.assertEqual(len(files), 1000)
        for file in files:
            with open(self.PATH_SOURCE + '\\' + file, 'w', encoding='utf-8') as f:
                f.write(file)
        copy_backup = CopyBackup(self.PATH_SOURCE + '\\', self.PATH_DESTINATION + '\\')
        copy_backup.copy_obj_all()
        directory = os.listdir(self.PATH_DESTINATION)

        for file in files:
            self.assertIn(file, directory)

            self.assertEqual(
                os.path.getsize(self.PATH_SOURCE + '\\' + file),
                os.path.getsize(self.PATH_DESTINATION + '\\' + file)
            )

    def test_copy_subproc(self):
        for file in self.files:
            with open(self.PATH_SOURCE + '\\' + file, 'w', encoding='utf-8') as f:
                f.write(file)
        copy_backup = CopyBackup(self.PATH_SOURCE + '\\', self.PATH_DESTINATION + '\\')
        copy_backup.copy_subproc_all()
        directory = os.listdir(self.PATH_DESTINATION)

        for file in self.files:
            self.assertIn(file, directory)

            self.assertEqual(
                os.path.getsize(self.PATH_SOURCE + '\\' + file),
                os.path.getsize(self.PATH_DESTINATION + '\\' + file)
            )

    def test_copy_subproc_big_files(self):
        big_files = ['big_file1.txt', 'big_file2.txt']
        for file in big_files:
            filler(self.PATH_SOURCE + '\\' + file)

        copy_backup = CopyBackup(self.PATH_SOURCE + '\\', self.PATH_DESTINATION + '\\')
        copy_backup.copy_subproc_all()
        directory = os.listdir(self.PATH_DESTINATION)

        for file in big_files:
            self.assertIn(file, directory)

            self.assertEqual(
                os.path.getsize(self.PATH_SOURCE + '\\' + file),
                os.path.getsize(self.PATH_DESTINATION + '\\' + file)
            )

    def test_subproc_load_by_quantity(self):
        files = [f'small_file_{i}.txt' for i in range(1,1001)]
        self.assertEqual(len(files), 1000)
        for file in files:
            with open(self.PATH_SOURCE + '\\' + file, 'w', encoding='utf-8') as f:
                f.write(file)
        copy_backup = CopyBackup(self.PATH_SOURCE + '\\', self.PATH_DESTINATION + '\\')
        copy_backup.copy_subproc_all()
        directory = os.listdir(self.PATH_DESTINATION)

        for file in files:
            self.assertIn(file, directory)

            self.assertEqual(
                os.path.getsize(self.PATH_SOURCE + '\\' + file),
                os.path.getsize(self.PATH_DESTINATION + '\\' +file)
            )

    def test_size_checking(self):
        files = [f'small_file_{i}.txt' for i in range(1, 1001)]
        self.assertEqual(len(files), 1000)
        for file in files:
            with open(self.PATH_SOURCE + '\\' + file, 'w', encoding='utf-8') as f:
                f.write(str(randint(1, 10_000_000)))
        copy_backup = CopyBackup(self.PATH_SOURCE + '\\', self.PATH_DESTINATION + '\\')
        folder_files = os.listdir(self.PATH_SOURCE)

        self.assertEqual(len(copy_backup.files), len(folder_files), len(files))
        copy_backup.copy_obj_all()
        directory = os.listdir(self.PATH_DESTINATION)
        self.assertEqual(len(folder_files), len(directory))

        for file in files:
            self.assertIn(file, directory)

            self.assertEqual(
                os.path.getsize(self.PATH_SOURCE + '\\' + file),
                os.path.getsize(self.PATH_DESTINATION + '\\' + file)
            )
        self.assertTrue(copy_backup.check_size())

    def test_deletion(self):
        files = [f'small_file_{i}.txt' for i in range(1, 1001)]
        for file in files:
            with open(self.PATH_SOURCE + '\\' + file, 'w', encoding='utf-8') as f:
                f.write(str(randint(1, 10_000_000)))

        source_folder_files_before_copy = os.listdir(self.PATH_SOURCE)
        destination_folder_before_copy = os.listdir(self.PATH_DESTINATION)
        self.assertEqual(len(source_folder_files_before_copy), 1000)
        self.assertEqual(len(destination_folder_before_copy), 0)

        copy_backup = CopyBackup(self.PATH_SOURCE + '\\', self.PATH_DESTINATION + '\\')
        copy_backup.copy_obj_all()

        source_folder_files_after_copy = os.listdir(self.PATH_SOURCE)
        destination_folder_after_copy = os.listdir(self.PATH_DESTINATION)
        self.assertEqual(len(source_folder_files_after_copy), 1000)
        self.assertEqual(len(destination_folder_after_copy), 1000)

        copy_backup.delete_origin()

        source_folder_files_after_copy = os.listdir(self.PATH_SOURCE)
        destination_folder_after_copy = os.listdir(self.PATH_DESTINATION)
        self.assertEqual(len(source_folder_files_after_copy), 0)
        self.assertEqual(len(destination_folder_after_copy), 1000)



    def tearDown(self):
        shutil.rmtree(self.PATH_SOURCE)
        shutil.rmtree(self.PATH_DESTINATION)


if __name__ == "__main__":
    unittest.main()