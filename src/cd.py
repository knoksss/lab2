import os
from src.logging_func import logging_func
from src.errors import PathError


def cd(inp_data):
    if not inp_data:
        error = "Не указан путь"
        logging_func(error)
        raise PathError(f'{error}')

    path = inp_data[0]
    if path == '~':
        path = os.path.expanduser('~')
    elif path == '..':
        path = '..'

    if os.path.exists(path) and os.path.isdir(path):
        os.chdir(path)
        return f"Находитесь здесь: {os.getcwd()}"
    else:
        error = "Путь не существует"
        logging_func(error)
        raise PathError(f'{error}')
