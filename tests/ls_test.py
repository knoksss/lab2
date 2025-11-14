import pytest
from unittest.mock import Mock, patch
from pathlib import Path
from src.ls import ls
from src.errors import PathError


class TestLs:
    def setup_method(self): # настраеваем тестовые переменные
        self.cwd = Path("/test/cwd")
        self.env = {}


    def test_ls_this_dir(self): # проверяем, как работает ls без аргументов
        test_files = ['file1.txt', 'file2.txt', 'directory1']
        # возвращает фейковую директорию и возвращает список тестовых файлов
        with patch('os.getcwd', return_value='/test/cwd'), \
             patch('os.path.exists', return_value=True), \
             patch('os.listdir', return_value=test_files), \
             patch('builtins.print') as mock_print:
            ls([])
            assert mock_print.call_count == 3 # проверяем, что функция была вызвана только три раза
            calls = [call[0][0] for call in mock_print.call_args_list] # проверяем конкретное содержание вызовов
            assert set(calls) == set(test_files) # проверяем, что выведены именно те файлы


    def test_ls_with_path(self): # проверяем ls с путём
        test_files = ['test.py', 'script.sh', 'data.json']
        with patch('os.getcwd', return_value='/test/cwd'), \
             patch('os.path.exists', return_value=True), \
             patch('os.listdir', return_value=test_files), \
             patch('builtins.print') as mock_print:
            ls(['/test/path'])
            # используем переданный путь вместо текущей директории
            assert mock_print.call_count == 3
            calls = [call[0][0] for call in mock_print.call_args_list]
            assert set(calls) == set(test_files)



    def test_ls_no_exist(self): # тестируем несуществующий путь
        with patch('os.getcwd', return_value='/test/cwd'), \
             patch('os.path.exists', return_value=False):
            with pytest.raises(PathError, match="ERROR: Путь не существует"):
                ls(['/nonexistent/path'])


    def test_ls_empty_dir(self): # тестируем пустую директорию
        with patch('os.getcwd', return_value='/test/cwd'), \
             patch('os.path.exists', return_value=True), \
             patch('os.listdir', return_value=[]), \
             patch('builtins.print') as mock_print:
            ls([])
            mock_print.assert_not_called()


    def test_ls_l(self): # тестируем с флагом -l
        test_files = ['file.txt']
        mock_stat = Mock() 
        mock_stat.st_size = 1234 # размер файла
        mock_stat.st_mtime = 1672531200 # дата изменения, но в развёртном числовом формате
        mock_stat.st_mode = 0o100644 # права доступа
        mock_datetime = Mock()
        mock_datetime.fromtimestamp.return_value = '2023-01-01 00:00:00' # преобразуем число в читаемую дату
        # задаём папку, в котрой находимся, возвращаем списко файлов, 
        # которые в ней находятся. используем команды, чтобы все пути выглядели, как
        # папка/файл, также инфорамцию о файле и преобразуем время в числовой формат
        with patch('os.getcwd', return_value='/test/cwd'), \
             patch('os.path.exists', return_value=True), \
             patch('os.listdir', return_value=test_files), \
             patch('os.path.join', side_effect=lambda p, f: f"{p}/{f}"), \
             patch('os.stat', return_value=mock_stat), \
             patch('src.ls.datetime', mock_datetime), \
             patch('builtins.print') as mock_print:
            ls(['-l'])
            mock_print.assert_called_once()
