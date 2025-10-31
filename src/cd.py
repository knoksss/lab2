import os
from src.logging_func import logging_func
from src.errors import PathError


def cd(inp_data):
    # проверяем указана ли директория
    if not inp_data:
        error = "Не указан путь"
        logging_func(error)
        raise PathError(f'{error}')
    
    # проверяем, что за путь
    path = inp_data[0]
    if path == '~':
        path = os.path.expanduser('~')
    elif path == '..':
        path = '..'

    if os.path.exists(path) and os.path.isdir(path): # проверяем существует ли и выводим сообщение, иначе ошибку
        os.chdir(path)
        return f"Находитесь здесь: {os.getcwd()}"
    else:
        error = "Путь не существует"
        logging_func(error)
        raise PathError(f'{error}')
