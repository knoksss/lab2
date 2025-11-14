import pytest
from unittest.mock import patch
from src.zip import zip, unzip
from src.errors import ExistError, FormatError, CreatingError

class TestZip:
    def test_zip_success(self): # проверяем, что архив был создан
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=True), \
             patch('shutil.make_archive', return_value=None) as mock_make, \
             patch('src.zip.logging_func') as mock_log:
            result = zip(['folder', 'archive'])
            mock_make.assert_called_once_with('archive', 'zip', 'folder')
            assert result == "Архив 'archive' создан"
            mock_log.assert_not_called() # проверяем, что это было успешно, потому что
            # не были вызваны никакие ошибки


    def test_zip_no_args(self): # проверяем, что выводит ошибки, если не указано, что архивировать
        with patch('src.zip.logging_func') as mock_log:
            with pytest.raises(ExistError, match="Не указано, что заархивировать и/или имя архива"):
                zip([])
            mock_log.assert_called_once()


    def test_zip_folder_not_exist(self): # проверяем, что выводит ошибку, если не существует папка
        with patch('os.path.exists', return_value=False), \
             patch('src.zip.logging_func') as mock_log:
            with pytest.raises(ExistError, match="Папка не существует"):
                zip(['folder', 'archive'])
            mock_log.assert_called_once()


    def test_zip_not_dir(self): # проверяем, что выводит ошибку, если пытаетмя заархивировать файл
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=False), \
             patch('src.zip.logging_func') as mock_log:
            with pytest.raises(FormatError, match="Несовместимый формат, архив создаётся из папки"):
                zip(['file.txt', 'archive'])
            mock_log.assert_called_once()


    def test_zip_create_error(self): # проверяем, что выводит ошибку в непредвиденных случаях
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=True), \
             patch('shutil.make_archive', side_effect=Exception("fail")), \
             patch('src.zip.logging_func') as mock_log:
            with pytest.raises(CreatingError, match="Произошла ошибка создания архива"):
                zip(['folder', 'archive'])
            mock_log.assert_called_once()


class TestUnzip:
    def test_unzip_success(self): # проверяем, что архив был успешно распакован
        with patch('os.path.exists', return_value=True), \
             patch('shutil.unpack_archive', return_value=None) as mock_unpack, \
             patch('src.zip.logging_func') as mock_log:
            result = unzip(['archive.zip'])
            mock_unpack.assert_called_once_with('archive.zip', '.')
            assert result == "Архив 'archive.zip' распакован"
            mock_log.assert_not_called()


    def test_unzip_no_args(self): # проверяем, что выводит ошибку, если не указано, что распкаовать
        with patch('src.zip.logging_func') as mock_log:
            with pytest.raises(ExistError, match="Не указан архив для распаковки"):
                unzip([])
            mock_log.assert_called_once()
            

    def test_unzip_archive_not_exist(self): # проверяем, что выводит ошибку, если пытаемся распаковать
        # несуществующий архив
        with patch('os.path.exists', return_value=False), \
             patch('src.zip.logging_func') as mock_log:
            with pytest.raises(ExistError, match="Архив не существует"):
                unzip(['archive.zip'])
            mock_log.assert_called_once()


    def test_unzip_unpack_error(self): # проверяем, что выводит ошибку в непредвиденных случаях
        with patch('os.path.exists', return_value=True), \
             patch('shutil.unpack_archive', side_effect=Exception("fail")), \
             patch('src.zip.logging_func') as mock_log:
            with pytest.raises(CreatingError, match="Произошла ошибка при распаковке архива"):
                unzip(['archive.zip'])
            mock_log.assert_called_once()