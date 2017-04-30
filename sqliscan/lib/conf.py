from lib.reader import FileReader

class settings:
    def __init__(self):
        self.sql_errors = FileReader("error.ini").read()

