import csv
import io


class CSVByteReader:
    def __init__(self, file):
        self.file = file
        self.file.seek(0)
        byte_string = self.file.read()
        string_io = io.StringIO(byte_string.decode("utf-8"))
        self.reader = csv.DictReader(string_io)

    def read_as_list_of_lists(self):
        return list(self.reader)

    def read_as_list_of_dicts(self):
        return [dict(row) for row in self.reader]
