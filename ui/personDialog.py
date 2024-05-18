import tkinter as tk
from tkinter import simpledialog
from models.person import Person

class PersonDialog(simpledialog.Dialog):
    def __init__(self, parent, title, data):
        self.data = data
        super().__init__(parent, title)

    def body(self, master):
        (tk.Label(master, text="Enter person's name and surname:")
         .grid(row=0, columnspan=2))
        tk.Label(master, text="Name:").grid(row=1)
        tk.Label(master, text="Surname:").grid(row=2)
        tk.Label(master, text="Birth surname:").grid(row=3)
        tk.Label(master, text="Born: (dd.mm.yyyy)").grid(row=4)
        tk.Label(master, text="Death: (dd.mm.yyyy)").grid(row=5)

        tk.Label(master, text="Parents").grid(row=6, column=0)

        self.couple_var = tk.StringVar(master)
        self.couple_var.set("Choose")

        couple_options = [f"{couple.family_surname} ({couple.marriage})" for couple in self.data.couples]
        if not couple_options:
            couple_options_options = ["No parent couples available"]
        self.couple_dropdown = tk.OptionMenu(master, self.couple_var,
                                             *couple_options)
        self.couple_dropdown.grid(row=6, column=1)

        self.name_entry = tk.Entry(master)
        self.surname_entry = tk.Entry(master)
        self.birth_surname = tk.Entry(master)
        self.born = tk.Entry(master)
        self.death = tk.Entry(master)

        self.name_entry.grid(row=1, column=1)
        self.surname_entry.grid(row=2, column=1)
        self.birth_surname.grid(row=3, column=1)
        self.born.grid(row=4, column=1)
        self.death.grid(row=5, column=1)

    def apply(self):
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        birth_surname = self.birth_surname.get()
        born_date = self.born.get()
        death_date = self.death.get()

        self.result = Person(name, surname, born=born_date,
                             death=death_date, birth_surname=birth_surname)
