import pytest
from unittest.mock import patch, mock_open
from src.grep import grep
from src.errors import FolderError, ExistError


class TestGrep:
    def setup_method(self):
        self.grep = grep
     

    def test_grep_file(self): # находит паттерн в файле
        file_content = "line 1\nHello world\nline 3"
        # создам фейковый файл с содержимым и читаем его,
        # а после перехваетываем вывод
        with patch('os.path.isfile', return_value=True), \
             patch('os.path.isdir', return_value=False), \
             patch('builtins.open', mock_open(read_data=file_content)), \
             patch('builtins.print') as mock_print:
            result = self.grep(['Hello', 'test.txt']) # функция с аргументами: паттерн и файл, в котром ищем
            assert result is None # команда не должна ничего выдать
            mock_print.assert_called_once_with('test.txt:2:Hello world') # а print должен был вызваться один раз с данными
            

    def test_grep_file_no_match(self): # тест, когда нет совпадений в файле
        file_content = "test 1 \n test 2"
        with patch('os.path.isfile', return_value=True), \
             patch('os.path.isdir', return_value=False), \
             patch('builtins.open', mock_open(read_data=file_content)), \
             patch('builtins.print') as mock_print:
            result = self.grep(['NotFound', 'test.txt'])
            assert result is None
            mock_print.assert_not_called() # проверяем, что print не был вызван, тк совпадений не было


    def test_grep_file_ignore(self): # игнорирование регистра
        file_content = "line 1\n hello world \n line 3"
        with patch('os.path.isfile', return_value=True), \
             patch('os.path.isdir', return_value=False), \
             patch('builtins.open', mock_open(read_data=file_content)), \
             patch('builtins.print') as mock_print:
            result = self.grep(['-i', 'HELLO', 'test.txt'])
            assert result is None
            mock_print.assert_called_once()


    def test_grep_directory_without_r(self): # ошибка, если хотим найти в директории что-то без -r
        with patch('os.path.isfile', return_value=False), \
             patch('os.path.isdir', return_value=True):
            with pytest.raises(FolderError, match='Используйте -r'): # смотрим, что выводит ошибку
                self.grep(['pattern', 'dir'])


    def test_grep_directory_with_r(self):
        file_content = "Hello\n world"
        # проверяем обход директории и возвращаем файл
        with patch('os.path.isfile', return_value=False), \
             patch('os.path.isdir', return_value=True), \
             patch('os.walk', return_value=[('dir', [], ['file.txt'])]), \
             patch('builtins.open', mock_open(read_data=file_content)), \
             patch('builtins.print') as mock_print:
            result = self.grep(['-r', 'Hello', 'dir'])
            assert result is None
            assert mock_print.called # проверяем, что print был вызван без проверки содержимого


    def test_grep_no_exist(self): # проверяем, что выдаёт ошибку на несуществующем файле
        with patch('os.path.isfile', return_value=False), \
             patch('os.path.isdir', return_value=False):
            with pytest.raises(ExistError, match='Не найдено'):
                self.grep(['pattern', 'no_exist'])


    def test_grep_empty(self): # проверяем, как функция работает с пустым файлом
        file_content = ""
        with patch('os.path.isfile', return_value=True), \
             patch('os.path.isdir', return_value=False), \
             patch('builtins.open', mock_open(read_data=file_content)), \
             patch('builtins.print') as mock_print:
            result = self.grep(['pattern', 'empty.txt'])
            assert result is None
            mock_print.assert_not_called() # проверяем, что функция не была вызвана


    def test_grep_somematches(self): # проверяем, что выведет, если будет несколько совпадений
        file_content = "Hello\nworld\nHello again"
        with patch('os.path.isfile', return_value=True), \
             patch('os.path.isdir', return_value=False), \
             patch('builtins.open', mock_open(read_data=file_content)), \
             patch('builtins.print') as mock_print:
            result = self.grep(['Hello', 'test.txt'])
            assert result is None
            assert mock_print.call_count == 2 # проверяем, что функция была вызвана ровно два раза
            calls = [call.args[0] for call in mock_print.call_args_list] # проверяем конкретное содержание вызовов
            assert calls == ['test.txt:1:Hello', 'test.txt:3:Hello again'] # проверяем, что совпадает
