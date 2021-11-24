import json
from node import node


class file_reader:
    data: list[node]

    def __init__(self, path) -> None:
        self.data = json.load(open(path, encoding='utf-8'))

    def get_data(self) -> list[node]:
        return self.data
