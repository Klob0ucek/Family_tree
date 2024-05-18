import tkinter as tk
from tkinter import messagebox

from models.data import Data
from models.userManager import UserManager
from ui.zoomableCanvas import ZoomableImageCanvas
from ui.personDialog import PersonDialog
from ui.coupleDialog import CoupleDialog

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700


class FamilyTreeUI:
    def __init__(self):
        self.user_manager = UserManager()
        self.user = None

        self.root = tk.Tk()
        self.root.title("Family Tree App")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(True, True)

        self.login_frame = tk.Frame(self.root)
        self.main_frame = tk.Frame(self.root)

        self.create_login_screen()
        self.create_main_screen()

        if self.user is None:
            self.show_login_screen()
        else:
            self.show_main_screen()

    def create_main_screen(self):
        self.main_frame.grid(row=0, column=0, sticky='nsew')
        self.add_person_button = tk.Button(self.main_frame, text="Add Person",
                                           command=self.add_person)
        self.add_person_button.grid(row=0, column=0, pady=10)

        self.add_couple_button = tk.Button(self.main_frame, text="Add Couple",
                                           command=self.add_couple)
        self.add_couple_button.grid(row=0, column=1, pady=10)

        self.draw_tree_button = tk.Button(self.main_frame, text="Reload Image",
                                          command=self.reload)
        self.draw_tree_button.grid(row=0, column=2, pady=10)

        self.save_button = tk.Button(self.main_frame, text="Save",
                                     command=self.save)
        self.save_button.grid(row=0, column=4, pady=10)

        self.leave_button = tk.Button(self.main_frame, text="Log out",
                                      command=self.log_out)
        self.leave_button.grid(row=0, column=5, pady=10)

        self.image_canvas = ZoomableImageCanvas(self.main_frame,
                                                width=(WINDOW_WIDTH - 20),
                                                height=(WINDOW_HEIGHT - 60),
                                                bg="white")
        self.image_canvas.grid(row=1, column=0, columnspan=6, padx=10)

    def create_login_screen(self):
        self.login_frame.grid(row=0, column=0, sticky='nsew')

        self.spacing = tk.Frame(self.login_frame, width=480)
        self.spacing.grid(row=0, column=0, pady=10)

        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.grid(row=0, column=1, pady=(250, 0))

        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=2, pady=(250, 0))

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=1, column=1, pady=10)

        self.password_entry = tk.Entry(self.login_frame, show='*')
        self.password_entry.grid(row=1, column=2, pady=10)

        self.login_button = tk.Button(self.login_frame, text="Login",
                                      command=self.login)
        self.login_button.grid(row=2, column=1, pady=10)

        self.register_button = tk.Button(self.login_frame, text="Register",
                                         command=self.register)
        self.register_button.grid(row=2, column=2, pady=10)

    def show_login_screen(self):
        self.main_frame.grid_forget()
        self.login_frame.grid()

    def show_main_screen(self):
        self.login_frame.grid_forget()
        self.main_frame.grid()
        self.image_canvas.reset_image(filename=self.user.get_file_name())

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        log_tup = self.user_manager.login_user(username, password)
        if log_tup:
            correct_password, logged_user = log_tup
            if (correct_password):
                messagebox.showinfo("Login Success", f"Welcome {username}")
                self.user = logged_user
                self.user.data.draw_family_tree(filename=self.user.get_file_name())
                self.show_main_screen()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")

        else:
            messagebox.showerror("Login Failed", "User not found not found")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.user_manager.register_user(username, password):
            messagebox.showinfo("Register Success", f"Welcome {username}")
            self.user = self.user_manager.login_user(username, password)
            self.show_main_screen()
        else:
            messagebox.showerror("Register Failed", "User already exists")

    def log_out(self):
        self.user = None
        self.show_login_screen()

    def add_person(self):
        name_dialog = PersonDialog(self.root, title="Add Person", data=self.user.data)
        result = name_dialog.result

        if result:
            self.user.data.people.append(result)
            self.user.data.draw_family_tree(filename=self.user.get_file_name())
            self.image_canvas.reset_image(filename=self.user.get_file_name())
            self.save_button.config(bg='red')

    def add_couple(self):
        couple_dialog = CoupleDialog(self.root, title="Add Couple",
                                     data=self.user.data)
        result = couple_dialog.result

        if result:
            self.user.data.couples.append(result)
            self.user.data.draw_family_tree(filename=self.user.get_file_name())
            self.image_canvas.reset_image(filename=self.user.get_file_name())
            self.save_button.config(bg='red')

    def reload(self):
        self.user.data.draw_family_tree(filename=self.user.get_file_name())
        self.image_canvas.reset_image(filename=self.user.get_file_name())

    def save(self):
        self.user_manager.save_users()
        self.root.after(100, lambda: self.save_button.config(bg='green'))

    def run(self):
        self.root.mainloop()
