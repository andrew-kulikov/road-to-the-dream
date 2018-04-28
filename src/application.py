from src import TaskList, User
import os
import json


class Application:
    users = {}
    cur_user = None

    @staticmethod
    def authorize(login, password):
        if login in Application.users:
            if Application.users[login].check_password(password):
                Application.cur_user = Application.users[login]
            else:
                raise KeyError('User does not exist')

    @staticmethod
    def register_user(name, login, password):
        if Application.users.get(login, None):
            raise KeyError('User with this login already exists')
        new_user = User(name, login, password)
        Application.users[login] = new_user
        Application.cur_user = new_user

    @staticmethod
    def save_users():
        if not os.path.exists('data\\'):
            os.mkdir('data\\')
        with open(os.path.join('data', 'users.txt'), 'w', encoding='utf-8') as f:
            f.write(json.dumps(Application.users))

    @staticmethod
    def load_users():
        if not os.path.exists('data\\'):
            os.mkdir('data\\')
            Application.users = None
        else:
            with open(os.path.join('data', 'users.txt'), 'r', encoding='utf-8') as f:
                print(json.loads(f.readline()))

    @staticmethod
    def save_task_list(task_list):
        if not os.path.exists('data\\'):
            os.mkdir('data\\')
        with open(os.path.join('data', task_list.name + '.txt'), 'w', encoding='utf-8') as f:
            f.write(json.dumps(task_list))
