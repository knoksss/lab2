import os
import docx2python
import pdfplumber
from src.logging_func import logging_func
from src.errors import FormatError
from src.errors import ExistError


def cat(inp_data: list) -> None:
    # если после cat ничего не ввели, то выводим ошибку
    if not inp_data:
        error = "Не указан файл, который нужно прочитать"
        logging_func(error)
        raise ExistError(f'{error}')
    
    # проверяем, если файл представляет собой папку и выводим ошибку, если это она
    file = inp_data[0]
    if os.path.isdir(file):
        error = "Несовместимый формат"
        logging_func(error)
        raise FormatError(f'{error}')

    # проверяем существование файла
    if not os.path.exists(file):
        error = "Файл не существует"
        logging_func(error)
        raise ExistError(f'{error}')
    
    # анализируем расширения файлов и выводим их содержимое, если возможно
    if '.txt' in file:
        f = open(file, 'r')
        print(f.read())

    elif '.docx' in file or '.doc' in file:
        docx_content = docx2python.docx2python(file)
        print(docx_content.text)

    elif '.pdf' in file:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                print(text)
    else:
        try:
            # для файлов с таким расширением, как .py, .lock и тд
            f = open(file, 'r') # если файл не удается вывести, то выводим ошибку
            print(f.read())
        except Exception as e:
            error = "Несовместимый формат"
            logging_func(error)
            raise FormatError(f'{error}')
