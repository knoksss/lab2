import pytest
from unittest.mock import patch
from pathlib import Path
from src.rm import rm
from src.errors import ExistError, FolderError, PathError


class TestRm:
    def setup_method(self): # настраеваем тестовые переменные
        self.cwd = Path("/test/cwd")
        self.env = {}


    def test_rm_no_input(self): # тест без указания данных
        with pytest.raises(ExistError, match="Не указано, что удалять"):
            rm([])


    def test_rm_r_no_path(self): # с флагом не указана директория, которую нужно удалить
        with pytest.raises(ExistError, match="Не указано, что удалять"):
            rm(['-r'])


    def test_rm_no_exist(self): # тест с несуществующим путём
        with patch('os.path.exists', return_value=False):
            with pytest.raises(PathError, match="Путь не существует"):
                rm(['no_exist.txt'])


    def test_rm_parent_directory(self): # попытка удаления родительской папки и выводим ошибку
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=True), \
             patch('os.path.abspath', side_effect=lambda x: '/test/parent' if x == '..' else f'/test/{x}'):
            # возвращает test/parent, если было введено ..
            # и возвращает другое, если не ..
            # сравнивает введённый путь с os.path.abspath
            with pytest.raises(FolderError, match="Нельзя удалять корневую или родительскую папку"):
                rm(['..'])


    def test_rm_dir_without_r(self): # проверяем, что выводит ошибку, если использовать без -r
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=True), \
             patch('os.path.abspath', side_effect=lambda x: '/test/directory' if x == 'test_directory' else f'/test/{x}'):
            with pytest.raises(FolderError, match="это папка, используйте -r"):
                rm(['test_directory'])


    def test_rm_file_yes(self): # тестируем, что удаляет файл, если ввести поддержи
        # проверяем, что ввод был yes или y, перехватываем вызов удаления и проверяем, что файл был удалён
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=False), \
             patch('os.path.abspath', side_effect=lambda x: '/test/file.txt' if x == 'file.txt' else f'/test/{x}'), \
             patch('builtins.input', return_value='yes'), \
             patch('os.remove') as mock_remove:
            result = rm(['file.txt'])
            mock_remove.assert_called_once_with('file.txt')
            assert result == "Файл 'file.txt' удален"


    def test_rm_file_no(self): # проверяем, что удаление отменяется, если мы введём команду отмены
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=False), \
             patch('os.path.abspath', side_effect=lambda x: '/test/file.txt' if x == 'file.txt' else f'/test/{x}'), \
             patch('builtins.input', return_value='no'):
            result = rm(['file.txt'])
            assert result == "Удаление отменено"
