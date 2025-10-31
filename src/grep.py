import os
import re
from src.logging_func import logging_func
from src.errors import FolderError
from src.errors import ExistError

def grep(inp_data):
    ig = False # переменная игнорирования регистра
    r = False # переменная для рекурсивного поиска
    
    # проверяем заданы ли нам две переменные, обозначеные выше
    if inp_data[0] == '-i':
        ig = True
        pattern = inp_data[1]
        path = inp_data[2]
    elif inp_data[0] == '-r':
        r = True
        pattern = inp_data[1]
        path = inp_data[2]
    else:
        pattern = inp_data[0]
        path = inp_data[1]

    if ig:
        flags = re.IGNORECASE # игнорируем регистр
    else:
        flags = 0
    regex = re.compile(pattern, flags) # функция для компиляции выражения

    # проверяем существует ли файл и проверяем есть ли в нём строка, соответствующая шаблону
    if os.path.isfile(path):
        with open(path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                if regex.search(line):
                    print(f"{path}:{i}:{line.rstrip()}")

    # проверяем существует ли папка и проверяем есть ли в ней файлы, в которых есть строки, удовл. шаблону
    elif os.path.isdir(path):
        if r:
            for root, dirs, files in os.walk(path):
                for file in files:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        for i, line in enumerate(f, 1):
                            if regex.search(line):
                                print(f"{os.path.join(root, file)}:{i}:{line.rstrip()}")
        # иначе выводим ошибки
        else:
            error = "Используйте -r"
            logging_func(error)
            raise FolderError(f'{error}')
    else:
        error = "Не найдено"
        logging_func(error)
        raise ExistError(f'{error}')