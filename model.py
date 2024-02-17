from graphviz import Graph
from uuid import uuid4, UUID
import json

class Data:
    def __init__(self, people=[], couples=[]):
        self.people = people
        self.couples = couples
        self.import_data("family_tree.json")
    
    def draw_family_tree(self):
        family_tree = Graph(comment='Family Tree')

        family_tree.attr('node', shape='box', rankdir='TB', fontname='Arial', splines='ortho')

        for person in self.people:
            family_tree.node(str(person.id), f'{person.name} {person.surname}\n* {person.born}\n T 20.2.2002')

        for couple in self.couples:
            with family_tree.subgraph(name=f'cluster_{str(couple.mother.id)}_{str(couple.father.id)}') as sg:
                sg.attr(label=f'{couple.family_surname}')
                sg.node(str(couple.mother.id), f'{couple.mother.name} {couple.mother.surname}')
                sg.node(str(couple.father.id), f'{couple.father.name} {couple.father.surname}')
                                
                sg.edge(str(couple.mother.id), str(couple.father.id), constraint='false')

            for child in couple.children:
                family_tree.edge(str(couple.mother.id), str(child.id))

        family_tree.render('family_tree', format='png', cleanup=True)
    
    def export_data(self, filename="family_tree.json"):
        data_dict = {
            "people": [
                {"id": str(person.id), "name": person.name, "surname": person.surname, "born": person.born, "death": person.death}
                for person in self.people
            ],
            "couples": [
                {
                    "mother_id": str(couple.mother.id),
                    "father_id": str(couple.father.id),
                    "family_surname": couple.family_surname,
                    "marriage": couple.marriage,
                    "children_ids": [str(child.id) for child in couple.children]
                }
                for couple in self.couples
            ]
        }

        with open(filename, "w") as file:
            json.dump(data_dict, file, indent=2)

    def import_data(self, filename):
        try:
            with open(filename, "r") as file:
                data_dict = json.load(file)
        except FileNotFoundError:
            # init json data
            p, c = test_data()
            self.people = p
            self.couples = c
            return

        self.people = [
            Person(
                name=person["name"],
                surname=person["surname"],
                born=person["born"],
                death=person["death"],
                id=UUID(person["id"])
            )
            for person in data_dict["people"]
        ]

        self.couples = [
            Couple(
                mother=self.find_person_by_id(UUID(couple["mother_id"])),
                father=self.find_person_by_id(UUID(couple["father_id"])),
                family_surname=couple["family_surname"],
                marriage=couple["marriage"],
                children=[self.find_person_by_id(UUID(child_id)) for child_id in couple["children_ids"]]
            )
            for couple in data_dict["couples"]
        ]

    def find_person_by_id(self, person_id):
        for person in self.people:
            if person.id == person_id:
                return person
        return None

    def find_person_by_name(self, name):
        for person in self.people:
            if person.get_name() == name:
                return person
        return None


class Person:
    def __init__(self, name, surname, id="", born="", death="", birth_surname="" ):
        self.name = name
        self.surname = surname
        self.id = id
        if id == "":
            self.id = uuid4()
        self.born = born
        self.death = death
        self.birth_surname = birth_surname #not exported/imported
        # rodné příjmení
    
    def get_name(self):
        return f"{self.name} {self.surname} ({self.born})"
    
    def node_data(self):
        return f'{person.name} {person.surname}\n* {person.born}\n T {person.death}'

class Couple:
    def __init__(self, mother, father, family_surname, marriage="1.1.2000", children=[]):
        self.mother = mother
        self.father = father
        self.family_surname = family_surname
        self.marriage = marriage
        self.children = children
        # datum svatby
        
def test_data():
    grandpa_pol = Person('Stanislav', 'Poláček', born="4.5.1947")
    grandma_pol = Person('Anežka', 'Poláčková', born="17.2.1949")
    grandpa = Person('Rostislav', 'Hvízdal', born="12.9.1943")
    uncle_pol = Person('Lukáš', 'Poláček', born="27.2.1974")
    aunt_pol = Person('Petra', 'Poláčková', born="14.7.1980")
    grandma = Person('Marie', 'Hvízdalová', born="30.7.1946")
    uncle = Person('Martina', 'Hvízdalová', born="10.7.1976")
    aunt = Person('Rostislav', 'Hvízdal', born="21.3.1969")
    mom = Person('Marie', 'Poláčková', born="4.5.1971")
    dad = Person('Stanislav', 'Poláček', born="4.5.1971")
    you = Person('Jan', 'Poláček', born="29.12.2002")
    sister = Person('Markéta', 'Poláčková', born="25.10.2005")
    brother = Person('Stanislav', 'Poláček', born="19.5.2000")
    luke = Person('Lukáš', 'Poláček', born="16.7.2003")
    zuzu = Person('Zuzana', 'Poláčková', born="26.9.2005")

    couple3 = Couple(mother=grandma_pol, father=grandpa_pol, family_surname="Poláčkovi", children=[dad, uncle_pol])
    couple1 = Couple(mother=grandma, father=grandpa, family_surname="Hvízdalovi", children=[mom, aunt, uncle])
    couple2 = Couple(mother=mom, father=dad, family_surname="Poláčkovi", children=[you, sister, brother])
    couple4 = Couple(mother=aunt_pol, father=uncle_pol, family_surname="Poláčkovi", children=[luke, zuzu])

    people = [grandpa, grandma, aunt, mom, dad, you, sister, brother, grandma_pol, grandpa_pol, uncle, uncle_pol, aunt_pol, luke, zuzu]
    couples = [couple1, couple2, couple3, couple4]
    return (people, couples)


def main():
    people, couples = test_data()
    data = Data(people, couples)
    data.draw_family_tree()
    data.export_data()
    

if __name__ == '__main__':
    main()