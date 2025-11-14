import pytest
from unittest.mock import patch
from src.cp import cp
from src.errors import PathError, ExistError, FormatError


class TestCp:
    def setup_method(self): # настраеваем тестовые переменные
        self.cp = cp
        

    def test_cp_file(self): # проверяем, что происходит копирование файла
        # перехватываем копирование файла и проверяем, что функция была вызвана
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=False), \
             patch('shutil.copy2') as mock_copy:
            result = self.cp(['file1.txt', 'file2.txt'])
            mock_copy.assert_called_once_with('file1.txt', 'file2.txt') # проверяем, что была вызвана функция с аргументами
            assert result == "Файл 'file1.txt' скопирован в 'file2.txt'" # проверяем вывод правильного сообщения


    def test_cp_directory_without_r(self): # проверяем, что выводит ошибку, когда хотим скопировать директорию без -r
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=True):
            with pytest.raises(FormatError, match='Несовместимый формат'): # проверяем, что выводит ошибку для заданных
                self.cp(['dir1', 'dir2'])


    def test_cp_directory_with_r_flag(self): # проверяем, что рекурсивное копирование работает
        # перехватываем функцию рекурсивного копирования
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=True), \
             patch('shutil.copytree') as mock_copytree:
            result = self.cp(['-r', 'dir1', 'dir2'])
            mock_copytree.assert_called_once_with('dir1', 'dir2')
            assert result == "Папка 'dir1' скопирована в 'dir2'"


    def test_cp_no_arguments(self): # тестируем, что выводит ошибку, когда нет аргументов
        with pytest.raises(ExistError, match='Не указано, куда и что копировать'):
            self.cp([])


    def test_cp_one_argument(self): # проверяем ошибку при указании одного аргумента
        with pytest.raises(ExistError, match='Не указано, куда и что копировать'):
            self.cp(['file1.txt'])


    def test_cp_r_flag_without_paths(self): # проверяем, что при не указании директории также выводит ошибку
        with pytest.raises(ExistError, match='Не указано, куда и что копировать'):
            self.cp(['-r'])


    def test_cp_r_flag_with_one_path(self):
        with pytest.raises(ExistError, match='Не указано, куда и что копировать'):
            self.cp(['-r', 'dir1'])


    def test_cp_nonexistent_source(self): # тестирование с несуществующим путём
        with patch('os.path.exists', return_value=False):
            with pytest.raises(PathError, match='Путь не существует'):
                self.cp(['no_file.txt', 'file2.txt'])
