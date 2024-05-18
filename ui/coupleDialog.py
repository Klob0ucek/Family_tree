import tkinter as tk
from tkinter import simpledialog
from models.couple import Couple
from ui.personDialog import PersonDialog


class CoupleDialog(simpledialog.Dialog):
    def __init__(self, parent, title, data):
        self.data = data
        self.selected_kids = []
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text="Choose paretns:").grid(row=0, columnspan=2)
        tk.Label(master, text="Mother:").grid(row=1)

        self.mother_var = tk.StringVar(master)
        self.mother_var.set("Choose")

        mother_options = [person.get_name() for person in self.data.people]
        if not mother_options:
            mother_options = ["No people available"]
        self.mother_dropdown = tk.OptionMenu(master, self.mother_var,
                                             *mother_options)
        self.mother_dropdown.grid(row=1, column=1)

        self.add_mother_button = tk.Button(master, text="Add Person",
                                           command=self.add_mother)
        self.add_mother_button.grid(row=1, column=2)

        tk.Label(master, text="Father:").grid(row=2)

        self.father_var = tk.StringVar(master)
        self.father_var.set("Choose")

        father_options = [person.get_name() for person in self.data.people]
        if not father_options:
            father_options = ["No people available"]
        self.father_dropdown = tk.OptionMenu(master, self.father_var,
                                             *father_options)
        self.father_dropdown.grid(row=2, column=1)

        self.add_father_button = tk.Button(master, text="Add Person",
                                           command=self.add_father)
        self.add_father_button.grid(row=2, column=2)

        tk.Label(master, text="Family surname:").grid(row=3)
        self.family_entry = tk.Entry(master, width=30)
        self.family_entry.grid(row=3, column=1, columnspan=2)

        tk.Label(master, text="Marriage date:").grid(row=4)
        self.marriage_date = tk.Entry(master, width=30)
        self.marriage_date.grid(row=4, column=1, columnspan=2)

        tk.Label(master, text="Children:").grid(row=5)
        self.kids_listbox = tk.Listbox(master, selectmode=tk.MULTIPLE,
                                       height=8, width=30)
        for person in self.data.people:
            self.kids_listbox.insert(tk.END, person.get_name())
        self.kids_listbox.grid(row=5, column=1, columnspan=2)

        self.add_child_button = tk.Button(master, text="Add Child",
                                          command=self.add_child)
        self.add_child_button.grid(row=6, column=1, columnspan=2)

    def apply(self):
        mother_name = self.mother_var.get()
        father_name = self.father_var.get()
        family_name = self.family_entry.get()
        marriage = self.marriage_date.get()

        selected_mother = self.data.find_person_by_name(mother_name)
        selected_father = self.data.find_person_by_name(father_name)
        selected_kids_indices = self.kids_listbox.curselection()

        self.selected_kids = [self.data.people[index] for index
                              in selected_kids_indices]
        if selected_mother is None or selected_father is None:
            self.result = None
        else:
            self.result = Couple(selected_mother, selected_father, family_name,
                                 marriage, self.selected_kids)

    def add_mother(self):
        self.add_person(self.mother_var)

    def add_father(self):
        self.add_person(self.father_var)

    def add_child(self):
        child_dialog = PersonDialog(self, title="Add Child", data=self.data)
        result = child_dialog.result

        if result:
            self.data.people.append(result)
            self.kids_listbox.insert(tk.END, result.get_name())

    def add_person(self, var):
        name_dialog = PersonDialog(self, title="Add Person", data=self.data)
        result = name_dialog.result

        if result:
            self.data.people.append(result)
            var.set(result.get_name())
            self.kids_listbox.insert(tk.END, result.get_name())
