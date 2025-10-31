import os
import shutil
from src.logging_func import logging_func
from src.errors import PathError
from src.errors import ExistError
from src.errors import FormatError


def cp(inp_data):
    if not inp_data or len(inp_data) < 2: # проверяем на наличие данных что и куда копировать
        error = "Не указано, куда и что копировать"
        logging_func(error)
        raise ExistError(f'{error}')

    # проверка для рекурсивного копирования
    if inp_data[0] == '-r':
        if len(inp_data) < 3:
            error = "Не указано, куда и что копировать"
            logging_func(error)
            raise ExistError(f'{error}')
        start = inp_data[1]
        finish = inp_data[2]
        r = True
    else:
        start = inp_data[0]
        finish = inp_data[1]
        r = False
    
    # проверка сущетсвует ли путь
    if not os.path.exists(start):
        error = "Путь не существует"
        logging_func(error)
        raise PathError(f'{error}')

    # проверяем папка ли это
    if os.path.isdir(start):
        if r: # проверяем есть ли метка о рекурсивном копировании
            shutil.copytree(start, finish)
            return f"Папка '{start}' скопирована в '{finish}'"
        else: #если нет, то выводим ошибку
            error = "Несовместимый формат"
            logging_func(error)
            raise FormatError(f'{error}')
    else: #если не папка, то копируем файл
        shutil.copy2(start, finish)
        return f"Файл '{start}' скопирован в '{finish}'"
