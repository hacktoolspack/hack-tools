

class FileReader:
    def __init__(self, file):
        """
        Reads the file content
        :param file: file to read
        """
        try:
            self.content = open(file).readlines()
        except IOError:
            raise FileNotFoundException

    def read(self):
        """
        returns the cleaned file content
        :return list: A list of content
        """
        return [line.strip("\n") for line in self.content]
