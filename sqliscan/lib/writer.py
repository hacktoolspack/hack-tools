from lib.cleaner import deduplicate


class FileWriter:
    def __init__(self, fileName, content):
        try:
            self.filename = fileName
            self.content = deduplicate(content).result
            self.write()
        except IOError:
            print("Unable to save {} file due to IOError".format(self.filename))

    def write(self):
        with open(self.filename, 'w') as cf:
            for line in self.content:
                cf.write(line+"\n")

