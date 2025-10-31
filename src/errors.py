class PathError(Exception):
    def __init__(self, *args):
        self.message = args[0]

    def __str__(self):
        return 'PathError, {0} '.format(self.message)


class ExistError(Exception):
    def __init__(self, *args):
        self.message = args[0]

    def __str__(self):
        return 'ExistError, {0} '.format(self.message)


class FolderError(Exception):
    def __init__(self, *args):
        self.message = args[0]

    def __str__(self):
        return 'FolderError, {0} '.format(self.message)


class FormatError(Exception):
    def __init__(self, *args):
        self.message = args[0]

    def __str__(self):
        return 'FormatError, {0} '.format(self.message)


class CreatingError(Exception):
    def __init__(self, *args):
        self.message = args[0]

    def __str__(self):
        return 'CreatingError, {0} '.format(self.message)
