import os
import shutil
from src.logging_func import logging_func
from src.errors import ExistError
from src.errors import FolderError
from src.errors import PathError


def rm(inp_data):
    if not inp_data:
        error = "Не указано, что удалять"
        logging_func(error)
        raise ExistError(f'{error}')

    # Проверяем есть ли опция -r
    if inp_data[0] == '-r':
        if len(inp_data) < 2:
            error = "Не указано, что удалять"
            logging_func(error)
            raise ExistError(f'{error}')
        folder = inp_data[1]
        r = True
    else:
        folder = inp_data[0]
        r = False

    if not os.path.exists(folder):
        error = "Путь не существует"
        logging_func(error)
        raise PathError(f'{error}')

    main_dir = os.path.abspath(folder)
    if main_dir == os.path.abspath('..'):
        error = "Нельзя удалять корневую или родительскую папку"
        logging_func(error)
        raise FolderError(f'{error}')

    if os.path.isdir(folder):
        if r:
            answer = input(
                f"Удалить папку '{folder}' и всё внутри? (yes/no): ")
            if answer.lower() in ['yes', 'y']:
                shutil.rmtree(folder)
                return f"Папка '{folder}' удалена"
            elif answer.lower() in ['no', 'n']:
                return "Удаление отменено"
            else:
                error = "ERROR: Неизвестная команда"
                logging_func(error)
                raise ValueError(f'{error}')
        else:
            error = f"'{folder}' это папка, используйте -r"
            logging_func(error)
            raise FolderError(f'{error}')
    else:
        answer = input(f"Удалить папку '{folder}' и всё внутри? (yes/no): ")
        if answer.lower() in ['yes', 'y']:
            os.remove(folder)
            return f"Файл '{folder}' удален"
        elif answer.lower() in ['no', 'n']:
            return "Удаление отменено"
        else:
            error = "ERROR: Неизвестная команда"
            logging_func(error)
            raise ValueError(f'{error}')
