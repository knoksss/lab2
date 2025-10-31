import os
from src.logging_func import logging_func
from src.errors import PathError
from src.errors import ExistError


def mv(inp_data):
    if not inp_data or len(inp_data) < 2:
        error = "Не указано, куда перемещать/как переименовать"
        logging_func(error)
        raise ExistError(f'{error}')

    start = inp_data[0]
    finish = inp_data[1]

    if not os.path.exists(start):
        error = "Путь не существует"
        logging_func(error)
        raise PathError(f'{error}')
    if finish.count('/') == 0:
        os.rename(start, finish)
        return f"'{start}' переименован в '{finish}'"
    else:
        os.rename(start, finish)
        return f"'{start}' перемещен в '{finish}'"
