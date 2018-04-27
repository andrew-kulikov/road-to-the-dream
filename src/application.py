from src import TaskList, User
import os
import json


class Application:
    users = {}
    cur_user = None

    @staticmethod
    def register_user(name, login, password):
        if Application.users.get(login, None):
            raise KeyError('User with this login already exists')
        Application.users[login] = User(name, login, password)

    @staticmethod
    def save_users():
        if not os.path.exists('data\\'):
            os.mkdir('data\\')
        with open(os.path.join('data', 'users.txt'), 'w', encoding='utf-8') as f:
            f.write(json.dumps(Application.users))
