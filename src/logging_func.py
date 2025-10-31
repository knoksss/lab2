import datetime

# открываем файл shell.log и записываем действия
def logging_func(command):
    with open('shell.log', 'a') as f:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{time}] {command}\n")
