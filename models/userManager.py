import json
import os
from hashlib import sha256

from models.user import User

USERS_FILE = "data/users.json"

class UserManager:
    def __init__(self):
        self.users = []
        self.load_users()
        if not self.register_user("admin", "admin"):
            print("User 'admin' already exists.")

    def load_users(self):
        self.users = []
        try:
            with open(USERS_FILE, 'r') as file:
                users_dict = json.load(file)
                for user in users_dict:
                    name = user.get('name')
                    password = user.get('password')
                    data_dict = user.get('data', {})
                    data_people = data_dict.get('people', [])
                    data_couples = data_dict.get('couples', [])
                    self.users.append(User(name, password, data_people, data_couples))
        except FileNotFoundError:
            self.users = []

    def register_user(self, username, password):
        hashed_password = sha256(password.encode()).hexdigest()
        if any(user.name == username for user in self.users):
            return False

        user = User(username, hashed_password)
        self.users.append(user)
        self.save_users()
        return True

    def login_user(self, username, password):
        hashed_password = sha256(password.encode()).hexdigest()
        for user in self.users:
            if user.name == username:
                return user.password == hashed_password, user
        return None

    def save_users(self):
        os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
        with open(USERS_FILE, 'w') as file:
            json.dump([user.export_data() for user in self.users], file, indent=2)
