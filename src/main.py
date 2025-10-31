from src.ls import ls
from src.cd import cd
from src.cat import cat
from src.cp import cp
from src.mv import mv
from src.rm import rm
from src.zip import zip
from src.zip import unzip
from src.tar import tar
from src.tar import untar
from src.grep import grep
from src.undo import undo
from src.logging_func import logging_func
from src.history import remember
from src.history import history

print('Введите команду. Для завершения введите: Стоп! Мне неприятно')

while True:
    try:
        entrance_str = input()

        if entrance_str == "Стоп! Мне неприятно":
            break
        if not entrance_str:
            continue

        remember(entrance_str)

        mas = entrance_str.split()
        cmd = mas[0]
        inp_data = mas[1:]

        if cmd == 'ls':
            logging_func(entrance_str)
            ls(inp_data)

        elif cmd == 'cd':
            logging_func(entrance_str)
            print(cd(inp_data))

        elif cmd == 'cat':
            logging_func(entrance_str)
            cat(inp_data)

        elif cmd == 'cp':
            logging_func(entrance_str)
            print(cp(inp_data))

        elif cmd == 'mv':
            logging_func(entrance_str)
            print(mv(inp_data))

        elif cmd == 'rm':
            logging_func(entrance_str)
            print(rm(inp_data))

        elif cmd == 'zip':
            logging_func(entrance_str)
            print(zip(inp_data))

        elif cmd == 'unzip':
            logging_func(entrance_str)
            print(unzip(inp_data))

        elif cmd == 'tar':
            logging_func(entrance_str)
            print(tar(inp_data))

        elif cmd == 'untar':
            logging_func(entrance_str)
            print(untar(inp_data))

        elif cmd == 'grep':
            logging_func(entrance_str)
            print(grep(inp_data))

        elif cmd == 'history':
            logging_func(entrance_str)
            print(history(inp_data))

        elif cmd == 'undo':
            logging_func(entrance_str)
            print(undo(inp_data))

        else:
            error = "ERROR: Неизвестная команда"
            logging_func(error)
            raise ValueError(f'{error}')

    except Exception as e:
        error = f"{str(e)}"
        print(error)
        logging_func(error)
