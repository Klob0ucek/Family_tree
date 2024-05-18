import json
from uuid import UUID
from models.person import Person
from models.couple import Couple

DEFAULT_FILE = "../data/family_tree.json"


class DataIO:
    def __init__(self, data):
        self.data = data

    def export_data(self, filename=DEFAULT_FILE):
        data_dict = {
            "people": [
                {
                    "id": str(person.id),
                    "name": person.name,
                    "surname": person.surname,
                    "born": person.born,
                    "death": person.death,
                    "birth_name": person.birth_surname}
                for person in self.data.people
            ],
            "couples": [
                {
                    "mother_id": str(couple.mother.id),
                    "father_id": str(couple.father.id),
                    "family_surname": couple.family_surname,
                    "marriage": couple.marriage,
                    "children_ids": [str(child.id) for child in couple.children]
                }
                for couple in self.data.couples
            ]
        }

        with open(filename, "w") as file:
            json.dump(data_dict, file, indent=2)

    def import_data(self, filename=DEFAULT_FILE):
        try:
            with open(DEFAULT_FILE, "r") as file:
                data_dict = json.load(file)
        except FileNotFoundError:
            return
        self.data.people = [
            Person(
                name=person["name"],
                surname=person["surname"],
                born=person["born"],
                death=person["death"],
                id=UUID(person["id"]),
                birth_surname=person["birth_name"]
            )
            for person in data_dict["people"]
        ]

        self.data.couples = [
            Couple(
                mother=self.data.find_person_by_id(UUID(couple["mother_id"])),
                father=self.data.find_person_by_id(UUID(couple["father_id"])),
                family_surname=couple["family_surname"],
                marriage=couple["marriage"],
                children=[self.data.find_person_by_id(UUID(child_id)) for child_id in couple["children_ids"]]
            )
            for couple in data_dict["couples"]
        ]
