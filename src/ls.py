import os
import datetime
from src.logging_func import logging_func
from src.errors import PathError


def ls(inp_data):

    path = os.getcwd()
    l_form = False

    for i in inp_data:
        if i == '-l':
            l_form = True
        else:
            path = i

    if not os.path.exists(path):
        error = "ERROR: Путь не существует"
        logging_func(error)
        raise PathError(f'{error}')

    if l_form:
        for i in os.listdir(path):
            i_path = os.path.join(path, i)
            info = os.stat(i_path)
            size = info.st_size
            ch_time = datetime.datetime.fromtimestamp(info.st_mtime)
            permissions = oct(info.st_mode)[-3:]
            print(f"{permissions} {size:8} {ch_time} {i}")
    else:
        for i in os.listdir(path):
            print(i)
