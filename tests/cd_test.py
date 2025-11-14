import pytest
from unittest.mock import patch
from pathlib import Path
from src.cd import cd
from src.errors import PathError


class TestCd:
    def setup_method(self): # настраеваем тестовые переменные
        self.cwd = Path("/test/cwd")
        self.env = {}


    def test_cd_path(self): # тестируем смену директории
        test_path = "/test/directory"
        # перехватываем смену директории и возвращаем путь
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=True), \
             patch('os.chdir') as mock_chdir, \
             patch('os.getcwd', return_value=test_path):
            
            result = cd([test_path])
            mock_chdir.assert_called_once_with(test_path) # проверяем, что смена директории произошла и это было 1 раз
            assert result == f"Находитесь здесь: {test_path}" # если переход был осуществлён, то должно вывести сообщени


    def test_cd_home_dir(self): # тестируем переход в домашнюю директорию
        home_path = "/test/directory"
        # преобразуем ~ в путь к домашней директории и проверяем перешли ли мы в неё
        with patch('os.path.expanduser', return_value=home_path), \
             patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=True), \
             patch('os.chdir') as mock_chdir, \
             patch('os.getcwd', return_value=home_path):
            
            result = cd(['~'])
            mock_chdir.assert_called_once_with(home_path)
            assert result == f"Находитесь здесь: {home_path}"


    def test_cd_parent_dir(self): # тестируем переход в родительскую директорию
        parent_path = "/test"
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=True), \
             patch('os.chdir') as mock_chdir, \
             patch('os.getcwd', return_value=parent_path):
            
            result = cd(['..'])
            mock_chdir.assert_called_once_with('..')
            assert result == f"Находитесь здесь: {parent_path}"


    def test_cd_no_path(self): # проверяем, что выводится ошибка, если не указан путь
        with pytest.raises(PathError, match="Не указан путь"):
            cd([])
            

    def test_cd_no_exist_path(self): # проверяем несуществующий путь
        with patch('os.path.exists', return_value=False):
            with pytest.raises(PathError, match="Путь не существует"):
                cd(['/no_exist/path'])


    def test_cd_file(self): # тестируем, что выводит ошибку, если хотим перейти в файл вместо директории
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=False):
            with pytest.raises(PathError, match="Путь не существует"):
                cd(['/path/file.txt'])
