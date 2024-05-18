from uuid import UUID

from models.couple import Couple
from models.data import Data
from models.person import Person


class User:
    def __init__(self, name, password, people=[], couples=[]):
        self.name = name
        self.password = password
        self.data = self.import_data(people, couples)

    def get_data(self):
        return self.data

    def get_file_name(self):
        return f"data/{self.name}_family_tree"

    def export_data(self):
        return {
            "name": self.name,
            "password": self.password,
            "data": self.data.export_data()
        }

    def import_data(self, people, couples):
        data = Data()
        data.people = [
            Person(
                name=person["name"],
                surname=person["surname"],
                born=person["born"],
                death=person["death"],
                id=UUID(person["id"]),
                birth_surname=person["birth_name"]
            )
            for person in people
        ]

        data.couples = [
            Couple(
                mother=data.find_person_by_id(UUID(couple["mother_id"])),
                father=data.find_person_by_id(UUID(couple["father_id"])),
                family_surname=couple["family_surname"],
                marriage=couple["marriage"],
                children=[data.find_person_by_id(UUID(child_id)) for child_id in couple["children_ids"]]
            )
            for couple in couples
        ]
        return data
