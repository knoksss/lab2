import os
import shutil
from src.logging_func import logging_func
from src.errors import ExistError
from src.errors import FormatError
from src.errors import CreatingError

# проверяем на сущетсвование папки и корректность данных
def zip(inp_data):
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

    try: # архивируем, в противном случае ошибка
        shutil.make_archive(inp_data[1], 'zip', inp_data[0])
        return f"Архив '{inp_data[1]}' создан"
    except Exception as e:
        error = "Произошла ошибка создания архива"
        logging_func(error)
        raise CreatingError(f'{error}')

# проверяем корректность введённых данных
def unzip(inp_data):
    if not inp_data:
        error = "Не указан архив для распаковки"
        logging_func(error)
        raise ExistError(f'{error}')

    if not os.path.exists(inp_data[0]):
        error = "Архив не существует"
        logging_func(error)
        raise ExistError(f'{error}')

    try: # разархивируем, в противном случае ошибка
        shutil.unpack_archive(inp_data[0], '.')
        return f"Архив '{inp_data[0]}' распакован"
    except Exception as e:
        error = "Произошла ошибка при распаковке архива"
        logging_func(error)
        raise CreatingError(f'{error}')
