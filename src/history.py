from src.logging_func import logging_func
from src.errors import ExistError

# открываем файл file.history для вывода построчно
def history(inp_data):
    try:
        history = open('file.history', 'r')
        f = history.readlines()
    except Exception as e:
        error = "Не использовано ни одной команды"
        logging_func(error)
        raise ExistError(f'{error}')
    
    for count, line in enumerate(f, 1):
        print(count, line.strip())

# записываем в файл новые данные о командах
def remember(inp_data):
    f = open('file.history', 'a')
    f.write(inp_data + '\n')