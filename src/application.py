from src import TaskList, User, Task
import os
import json
import pickle


class Application:
    users = {}
    cur_user = None

    @staticmethod
    def authorize(login, password):
        if login in Application.users:
            if Application.users[login].check_password(password):
                Application.cur_user = Application.users[login]
            else:
                raise KeyError('Wrong password')
        else:
            raise KeyError('User does not exist')

    @staticmethod
    def register_user(name, login, password):
        if Application.users.get(login, None):
            raise KeyError('User with this login already exists')
        new_user = User(login, password, name)
        Application.users[login] = new_user
        Application.cur_user = new_user

    @staticmethod
    def save_users():
        if not os.path.exists('data\\'):
            os.mkdir('data\\')
        with open(os.path.join('data', 'users.pkl'), 'wb+') as f:
            pickle.dump(Application.users, f, pickle.HIGHEST_PROTOCOL)
        with open(os.path.join('data', 'cur_user.txt'), 'w', encoding='utf-8') as f:
            if Application.cur_user:
                f.write(Application.cur_user.login)

    @staticmethod
    def load_users():
        if not os.path.exists('data\\'):
            os.mkdir('data\\')
            Application.users = None
        elif os.path.exists(os.path.join('data', 'users.pkl')):
            with open(os.path.join('data', 'users.pkl'), 'rb+') as f:
                Application.users = pickle.load(f)
        Application.load_cur_user()

    @staticmethod
    def save_task_list(task_list):
        if not os.path.exists('data\\'):
            os.mkdir('data\\')
        with open(os.path.join('data', task_list.name + '.txt'), 'w', encoding='utf-8') as f:
            f.write(json.dumps(task_list))

    @staticmethod
    def load_cur_user():
        if not os.path.exists(os.path.join('data', 'cur_user.txt')):
            open(os.path.join('data', 'cur_user.txt'), 'w').close()
            Application.cur_user = None
        else:
            with open(os.path.join('data', 'cur_user.txt'), 'r', encoding='utf-8') as f:
                try:
                    Application.cur_user = Application.users[f.readline().strip()]
                except KeyError as e:
                    Application.cur_user = None

    @staticmethod
    def add_task(name, description, tags, parent_id=0):
        task = Task(name=name, description=description, tags=tags, parent_id=parent_id)
        Application.cur_user.add_task(task)

    @staticmethod
    def complete_task(task_id):
        try:
            Application.cur_user.complete_task(task_id)
        except KeyError as e:
            raise e
        except AttributeError as e:
            raise e

    @staticmethod
    def move_task(source_id, destination_id):
        try:
            Application.cur_user.move_task(source_id, destination_id)
        except KeyError as e:
            raise e
        except RecursionError as e:
            raise e

    @staticmethod
    def run():
        Application.load_users()
