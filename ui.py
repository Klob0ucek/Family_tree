import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import simpledialog

from model import Data, Person, Couple
from model import test_data

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

class PersonDialog(simpledialog.Dialog): # TODO - need to be change if Person changes
    def __init__(self, parent, title):
        super().__init__(parent, title)
        
    def body(self, master):
        tk.Label(master, text="Enter person's name and surname:").grid(row=0, columnspan=2)
        tk.Label(master, text="Name:").grid(row=1)
        tk.Label(master, text="Surname:").grid(row=2)
        tk.Label(master, text="Birth surname:").grid(row=3)
        tk.Label(master, text="Born: (dd.mm.yyyy)").grid(row=4)
        tk.Label(master, text="Death: (dd.mm.yyyy)").grid(row=5)

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
        
        self.result = Person(name, surname, born=born_date, death=death_date, birth_surname=birth_surname)


class CoupleDialog(simpledialog.Dialog): # TODO - need to be change if Couple changes
    def __init__(self, parent, title, data):
        self.data = data
        self.selected_kids = []
        super().__init__(parent, title)

    def body(self, master): # Add new Person for mother/father
        tk.Label(master, text="Choose paretns:").grid(row=0, columnspan=2)
        tk.Label(master, text="Mother:").grid(row=1)

        self.mother_var = tk.StringVar(master)
        self.mother_var.set("Choose")

        mother_options = [person.get_name() for person in self.data.people]
        if not mother_options:
            mother_options = ["No people available"]
        self.mother_dropdown = tk.OptionMenu(master, self.mother_var, *mother_options)
        self.mother_dropdown.grid(row=1, column=1)
        
        self.add_mother_button = tk.Button(master, text="Add Person", command=self.add_mother)
        self.add_mother_button.grid(row=1, column=2)

        tk.Label(master, text="Father:").grid(row=2)

        self.father_var = tk.StringVar(master)
        self.father_var.set("Choose")

        father_options = [person.get_name() for person in self.data.people]
        if not father_options:
            father_options = ["No people available"]
        self.father_dropdown = tk.OptionMenu(master, self.father_var, *father_options)
        self.father_dropdown.grid(row=2, column=1)
        
        self.add_father_button = tk.Button(master, text="Add Person", command=self.add_father)
        self.add_father_button.grid(row=2, column=2)
        
        tk.Label(master, text="Family surname:").grid(row=3)
        self.family_entry = tk.Entry(master, width=30)
        self.family_entry.grid(row=3, column=1, columnspan=2)
        
        tk.Label(master, text="Marriage date:").grid(row=4)
        self.marriage_date = tk.Entry(master, width=30)
        self.marriage_date.grid(row=4, column=1, columnspan=2)
        
        tk.Label(master, text="Children:").grid(row=5)
        self.kids_listbox = tk.Listbox(master, selectmode=tk.MULTIPLE, height=8, width=30)
        for person in self.data.people:
            self.kids_listbox.insert(tk.END, person.get_name())
        self.kids_listbox.grid(row=5, column=1, columnspan=2)
        
        self.add_child_button = tk.Button(master, text="Add Child", command=self.add_child)
        self.add_child_button.grid(row=6, column=1, columnspan=2)

        # TODO Add other couple atributes

    def apply(self):
        mother_name = self.mother_var.get()
        father_name = self.father_var.get()
        family_name = self.family_entry.get()
        marriage = self.marriage_date.get()
        
        selected_mother = self.data.find_person_by_name(mother_name)
        selected_father = self.data.find_person_by_name(father_name)
        selected_kids_indices = self.kids_listbox.curselection()
        
        self.selected_kids = [self.data.people[index] for index in selected_kids_indices]
        if selected_mother is None or selected_father is None:
            self.result = None
        else:
            self.result = Couple(selected_mother, selected_father, family_name, marriage, self.selected_kids)
    
    def add_mother(self):
        self.add_person(self.mother_var)
    
    def add_father(self):
        self.add_person(self.father_var)
        
    def add_child(self):
        # Create a new person and add it to the children list
        child_dialog = PersonDialog(self, title="Add Child")
        result = child_dialog.result

        if result:
            self.data.people.append(result)
            self.kids_listbox.insert(tk.END, result.get_name())

    def add_person(self, var): # copy of a method
        name_dialog = PersonDialog(self, title="Add Person")
        result = name_dialog.result

        if result:
            self.data.people.append(result)
            var.set(result.get_name())
            self.kids_listbox.insert(tk.END, result.get_name())


class ZoomableImageCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
        self.image = None
        self.image_ref = None
        self.zoom_factor = 1.0
        self.pan_start_x = 0
        self.pan_start_y = 0

        self.bind("<MouseWheel>", self._on_mousewheel)
        self.bind("<Button-4>", self._on_mousewheel)  # Linux
        self.bind("<Button-5>", self._on_mousewheel)  # Linux
        self.bind("<ButtonPress-1>", self._start_pan)
        self.bind("<B1-Motion>", self._pan_image)

    def load_image(self):
        image_path = "family_tree.png"
        image = Image.open(image_path)
        self.image_ref = ImageTk.PhotoImage(image)
        self.image = self.create_image(0, 0, anchor=tk.NW, image=self.image_ref)

    def _on_mousewheel(self, event):
        if event.delta > 0:
            self.zoom_in()
        elif event.delta < 0:
            self.zoom_out()

    def zoom_in(self):
        self.zoom_factor *= 1.1
        self._apply_zoom()

    def zoom_out(self):
        self.zoom_factor /= 1.1
        self._apply_zoom()

    def _apply_zoom(self):
        new_width = int(self.image_ref.width() * self.zoom_factor)
        new_height = int(self.image_ref.height() * self.zoom_factor)

        image = Image.open("family_tree.png")
        image_resized = image.resize((new_width, new_height), Image.LANCZOS)
        self.image_ref = ImageTk.PhotoImage(image_resized)
        self.itemconfig(self.image, image=self.image_ref)

    def _start_pan(self, event):
        self.pan_start_x = event.x
        self.pan_start_y = event.y

    def _pan_image(self, event):
        delta_x = event.x - self.pan_start_x
        delta_y = event.y - self.pan_start_y

        self.scan_mark(0, 0)  # Reset the scan mark
        self.scan_dragto(delta_x, delta_y, gain=1)

        self.pan_start_x = event.x
        self.pan_start_y = event.y

    def reset_image(self):
        self.zoom_factor = 1.0
        self.load_image()


class FamilyTreeUI:
    def __init__(self, data):
        self.data = data

        self.root = tk.Tk()
        self.root.title("Family Tree App")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(True, True)

        self.add_person_button = tk.Button(self.root, text="Add Person", command=self.add_person)
        self.add_person_button.grid(row=0, column=0, pady=10)

        self.add_couple_button = tk.Button(self.root, text="Add Couple", command=self.add_couple)
        self.add_couple_button.grid(row=0, column=1, pady=10)

        self.draw_tree_button = tk.Button(self.root, text="Reload Image", command=self.reload)
        self.draw_tree_button.grid(row=0, column=2, pady=10)
        
        self.save_button = tk.Button(self.root, text="Save", comman=self.save)
        self.save_button.grid(row=0, column=4, pady=10)
        
        self.image_canvas = ZoomableImageCanvas(self.root, width=(WINDOW_WIDTH - 20), height=(WINDOW_HEIGHT - 60), bg="white")
        self.image_canvas.grid(row=1, column=0, columnspan=5, padx=10)

        self.image_canvas.load_image()

    def add_person(self):
        name_dialog = PersonDialog(self.root, title="Add Person")
        result = name_dialog.result

        # maybe some validation??
        if result:
            self.data.people.append(result)
            self.data.draw_family_tree()
            self.image_canvas.reset_image()
            self.save_button.config(bg='red')
            

    def add_couple(self):
        couple_dialog = CoupleDialog(self.root, title="Add Couple", data=self.data)
        result = couple_dialog.result

        # maybe some validation??
        if result:
            self.data.couples.append(result)
            self.data.draw_family_tree()
            self.image_canvas.reset_image()
            self.save_button.config(bg='red')
    
    def reload(self):
        self.data.draw_family_tree()
        self.image_canvas.reset_image()
    
    def save(self):
        self.data.export_data()
        self.root.after(100, lambda: self.save_button.config(bg='green'))
        
    def run(self):
        self.root.mainloop()


if __name__ == "__main__": # maybe move this to main.py?
    data = Data([], [])
    family_tree_ui = FamilyTreeUI(data)
    family_tree_ui.run()

