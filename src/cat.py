import os
import docx2python
import pdfplumber
from src.logging_func import logging_func
from src.errors import FormatError
from src.errors import ExistError


def cat(inp_data: list) -> None:
    if not inp_data:
        error = "Не указан файл, который нужно прочитать"
        logging_func(error)
        raise ExistError(f'{error}')

    file = inp_data[0]
    if os.path.isdir(file):
        error = "Несовместимый формат"
        logging_func(error)
        raise FormatError(f'{error}')

    if not os.path.exists(file):
        error = "Файл не существует"
        logging_func(error)
        raise ExistError(f'{error}')

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
            f = open(file, 'r')
            print(f.read())
        except Exception as e:
            error = "Несовместимый формат"
            logging_func(error)
            raise FormatError(f'{error}')
