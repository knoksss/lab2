import pytest
from unittest.mock import patch, mock_open
from pathlib import Path
from src.cat import cat
from src.errors import ExistError, FormatError


class TestCat:
    def setup_method(self): # настраеваем тестовые переменные
        self.cwd = Path("/test/cwd") 
        self.env = {} 


    def test_cat_file(self): # тестируем чтение файла
        file_content = "Hello, world!"
        # создаём заглушку для функции open, которая возвращает содержимое файла
        # и перехватываем функцию print до того, как она что-то вывела
        with patch('builtins.open', mock_open(read_data=file_content)), \
             patch('os.path.exists', return_value=True), \
             patch('os.path.isfile', return_value=True), \
             patch('builtins.print') as mock_print:
            
            cat(['test.txt'])
            mock_print.assert_called_once() # убеждаемся, что print был вызван один раз


    def test_cat_no_exist(self): # тест с несуществующим файлов: должен вывести ошибку
        with patch('os.path.exists', return_value=False):
            with pytest.raises(ExistError, match="Файл не существует"):
                cat(['no_exist.txt'])


    def test_cat_inp_problem(self): # тест без указания файла, который нужно прочитать
        with pytest.raises(ExistError, match="Не указан файл, который нужно прочитать"):
            cat([])


    def test_cat_dir(self): # тест с несовместимым форматом: прочитать директорию невозможно
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=True):
            
            with pytest.raises(FormatError, match="Несовместимый формат"):
                cat(['some_directory'])
