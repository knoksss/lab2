import os
import tarfile
from src.logging_func import logging_func
from src.errors import ExistError
from src.errors import FormatError
from src.errors import CreatingError


def tar(inp_data):
    if not inp_data or len(inp_data) < 2:
        error = "Не указано, что заархивировать и/или имя архива"
        logging_func(error)
        raise ExistError(f'{error}')

    if not os.path.exists(inp_data[0]):
        error = "Папка не существует"
        logging_func(error)
        raise ExistError(f'{error}')

    if not os.path.isdir(inp_data[0]):
        error = "Несовместимый формат, архив создаётся из папки"
        logging_func(error)
        raise FormatError(f'{error}')

    if not inp_data[1].endswith('.tar.gz'):
        inp_data[1] += '.tar.gz'

    try:
        with tarfile.open(inp_data[1], "w:gz") as tar:
            tar.add(inp_data[0], arcname=os.path.basename(inp_data[0]))
        return f"Архив '{inp_data[0]}' создан"
    except Exception as e:
        error = "Произошла ошибка создания архива"
        logging_func(error)
        raise CreatingError(f'{error}')


def untar(inp_data):
    this_dir = os.getcwd()

    if not inp_data:
        return "Укажите архив для распаковки"

    if not inp_data[0].endswith('.tar.gz'):
        inp_data[0] += '.tar.gz'

    if not os.path.exists(inp_data[0]):
        error = f"Ошибка: архив '{inp_data[0]}' не существует"
        logging_func(error)
        return error

    try:
        with tarfile.open(inp_data[0], 'r') as tar:
            tar.extractall(this_dir)

    except Exception as e:
        error = "Произошла ошибка при распаковке архива"
        logging_func(error)
        raise CreatingError(f'{error}')
