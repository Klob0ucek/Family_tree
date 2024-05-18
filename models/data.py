from graphviz import Graph

from models.person import Person
from models.couple import Couple


class Data:
    def __init__(self, people=[], couples=[]):
        self.people = people
        self.couples = couples

    def draw_family_tree(self, filename):
        family_tree = Graph(comment='Family Tree')

        family_tree.attr('node', shape='box', rankdir='TB', fontname='Arial', splines='ortho')
        family_tree.attr(ranksep='1.2', nodesep='0.4')

        for person in self.people:
            family_tree.node(str(person.id), person.node_data())

        for couple in self.couples:
            with family_tree.subgraph(name=f'cluster_{str(couple.mother.id)}_{str(couple.father.id)}') as sg:
                sg.attr(label=f'{couple.family_surname}')
                sg.node(str(couple.mother.id), couple.mother.node_data())
                sg.node(str(couple.father.id), couple.father.node_data())
                sg.edge(str(couple.mother.id), str(couple.father.id), constraint='false')

            for child in couple.children:
                family_tree.edge(str(couple.mother.id), str(child.id))

        family_tree.render(filename, format='png', cleanup=True)

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

    def export_data(self):
        return {
            "people": [
                {
                    "id": str(person.id),
                    "name": person.name,
                    "surname": person.surname,
                    "born": person.born,
                    "death": person.death,
                    "birth_name": person.birth_surname}
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


def test_data():
    grandpa_pol = Person('Stanislav', 'Poláček', born="4.5.1947")
    grandma_pol = Person('Anežka', 'Poláčková', born="17.2.1949", birth_surname="Konečná")
    grandpa_hviz = Person('Rostislav', 'Hvízdal', born="12.9.1943")
    uncle_pol = Person('Lukáš', 'Poláček', born="27.2.1974")
    aunt_pol = Person('Petra', 'Poláčková', born="14.7.1980", birth_surname="Fricová")
    grandma_hviz = Person('Marie', 'Hvízdalová', born="30.7.1946", birth_surname="Sedláčková")
    uncle = Person('Martina', 'Hvízdalová', born="10.7.1976")
    aunt = Person('Rostislav', 'Hvízdal', born="21.3.1969")
    mom = Person('Marie', 'Poláčková', born="4.5.1971", birth_surname="Hvízdalová")
    dad = Person('Stanislav', 'Poláček', born="4.5.1971")
    you = Person('Jan', 'Poláček', born="29.12.2002")
    sister = Person('Markéta', 'Poláčková', born="25.10.2005")
    brother = Person('Stanislav', 'Poláček', born="19.5.2000")
    luke = Person('Lukáš', 'Poláček', born="16.7.2003")
    zuzu = Person('Zuzana', 'Poláčková', born="26.9.2005")

    couple3 = Couple(mother=grandma_pol, father=grandpa_pol, family_surname="Poláčkovi", children=[dad, uncle_pol])
    couple1 = Couple(mother=grandma_hviz, father=grandpa_hviz, family_surname="Hvízdalovi", children=[mom, aunt, uncle])
    couple2 = Couple(mother=mom, father=dad, family_surname="Poláčkovi", children=[you, sister, brother])
    couple4 = Couple(mother=aunt_pol, father=uncle_pol, family_surname="Poláčkovi", children=[luke, zuzu])

    people = [grandpa_hviz, grandma_hviz, aunt, mom, dad, you, sister, brother, grandma_pol, grandpa_pol, uncle, uncle_pol, aunt_pol, luke, zuzu]
    couples = [couple1, couple2, couple3, couple4]
    return (people, couples)
