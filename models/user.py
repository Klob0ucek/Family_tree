from models.data import Data


class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.data = Data([], [])

    def get_data(self):
        return self.data