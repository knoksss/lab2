import pytest
from unittest.mock import patch
from pathlib import Path
from src.mv import mv
from src.errors import PathError, ExistError


class TestMv:
    def setup_method(self): # настраеваем тестовые переменные
        self.cwd = Path("/test/cwd")
        self.env = {}


    def test_mv_rename_file(self): # переименовываем файл
        # перехватываем переименовывание файла
        with patch('os.path.exists', return_value=True), \
             patch('os.rename') as mock_rename, \
             patch('builtins.print') as mock_print:
            result = mv(['old_name.txt', 'new_name.txt'])
            mock_rename.assert_called_once_with('old_name.txt', 'new_name.txt') # проверяем, что фукция была вызвана один раз
            assert result == "'old_name.txt' переименован в 'new_name.txt'" # проверяем, что вывело именно это


    def test_mv_move_file(self): # премещение в другую директорию
        with patch('os.path.exists', return_value=True), \
             patch('os.rename') as mock_rename, \
             patch('builtins.print') as mock_print:
            result = mv(['file.txt', '/new/directory/file.txt'])
            mock_rename.assert_called_once_with('file.txt', '/new/directory/file.txt')
            assert result == "'file.txt' перемещен в '/new/directory/file.txt'"


    def test_mv_rename_dir(self): # переменовываем директорию
        with patch('os.path.exists', return_value=True), \
             patch('os.rename') as mock_rename, \
             patch('builtins.print') as mock_print:
            result = mv(['old_dir', 'new_dir'])
            mock_rename.assert_called_once_with('old_dir', 'new_dir')
            assert result == "'old_dir' переименован в 'new_dir'"


    def test_mv_move_directory_with_path(self): # перемещение директории
        with patch('os.path.exists', return_value=True), \
             patch('os.rename') as mock_rename, \
             patch('builtins.print') as mock_print:
            result = mv(['my_folder', '/backup/my_folder'])
            mock_rename.assert_called_once_with('my_folder', '/backup/my_folder')
            assert result == "'my_folder' перемещен в '/backup/my_folder'"


    def test_mv_no_arguments(self): # тест без указания, что перемещать и куда
        with pytest.raises(ExistError, match="Не указано, куда перемещать/как переименовать"):
            mv([])


    def test_mv_one_argument(self): # тест с одним аргументом вместо двух
        with pytest.raises(ExistError, match="Не указано, куда перемещать/как переименовать"):
            mv(['file.txt'])


    def test_mv_no_exist(self): # тест с несуществующим файлом
        with patch('os.path.exists', return_value=False):
            with pytest.raises(PathError, match="Путь не существует"):
                mv(['no_exist.txt', 'new_name.txt'])
