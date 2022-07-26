from typing import OrderedDict


class Command():
    def __init__(self, type, data=None) -> None:
        self.type = type
        self.data = data

    def get_type(self):
        return self.type

    def __repr__(self) -> str:
        return f"Command({self.type}, {self.data})"


    def get_data_piece_i(self, index):
        if type(self.data) == list:
            return self.data[index]
        
        if type(self.data) == OrderedDict:
            return list(self.data.items)[index]