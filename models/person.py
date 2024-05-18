from uuid import uuid4

class Person:
    def __init__(self, name, surname, id="", born="", death="", birth_surname=""):
        self.name = name
        self.surname = surname
        self.id = id
        if id == "":
            self.id = uuid4()
        self.born = born
        self.death = death
        self.birth_surname = birth_surname

    def get_name(self):
        return f"{self.name} {self.surname} ({self.born})"

    def node_data(self):
        birth_name = f"({self.birth_surname})" if self.birth_surname != "" else ""
        death = f"\n+ {self.death}" if self.death else ""
        return f'{self.name} {birth_name} {self.surname}\n* {self.born}{death}'
