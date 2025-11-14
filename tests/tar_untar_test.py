import pytest
from unittest.mock import patch, MagicMock
from src.tar import tar, untar
from src.errors import ExistError, FormatError, CreatingError

class TestTarUntar:
    def test_tar_no_args(self): # проверяем, что выводит ошибку, если не введено ничего
        with pytest.raises(ExistError, match="Не указано, что заархивировать и/или имя архива"):
                tar([])


    def test_tar_folder_not_exist(self): # проверяем, что выводит ошибку на несуществующий файл
        with patch('os.path.exists', return_value=False):
            with pytest.raises(ExistError, match="Папка не существует"):
                tar(['folder', 'archive'])


    def test_tar_not_dir(self): # проверяем, что выводит ошибку, если пытаемся заархивировать файл
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=False):
            with pytest.raises(FormatError, match="Несовместимый формат, архив создаётся из папки"):
                tar(['file.txt', 'archive'])


    def test_tar_success(self): # проверяем, что работает архивирование
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=True), \
             patch('tarfile.open', MagicMock()) as mock_tar_open:
            result = tar(['folder', 'archive'])
            assert result.startswith("Архив")
            mock_tar_open.assert_called_once()


    def test_tar_creating_error(self): # проверяем, что выводит ошибку во всех непредвиденных случаях
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=True), \
             patch('tarfile.open', side_effect=Exception("fail")):
                with pytest.raises(CreatingError, match="Произошла ошибка создания архива"):
                    tar(['folder', 'archive'])


    def test_untar_no_args(self): # проверяем, что выводит сообщение, если не указан архив
        result = untar([])
        assert result == "Укажите архив для распаковки"


    def test_untar_archive_not_exist(self): # проверяем, что выводит, если не существует путь
        with patch('os.path.exists', return_value=False):
            result = untar(['archive'])
            assert "Ошибка: архив" in result


    def test_untar_success(self): # проверяем, что архив был успешно распакован
        mock_tar = MagicMock()
        with patch('os.path.exists', return_value=True), \
             patch('tarfile.open', return_value=mock_tar):
            result = untar(['archive'])
            assert result is None


    def test_untar_creating_error(self): # проверяем,что выводит ошибку в непредвиденных ситуациях
        with patch('os.path.exists', return_value=True), \
             patch('tarfile.open', side_effect=Exception("fail")):
            with pytest.raises(CreatingError, match="Произошла ошибка при распаковке архива"):
                untar(['archive'])
