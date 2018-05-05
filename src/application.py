from src import TaskList, User, Task, Project, ProjectTask
import os
import json
import pickle
import jsonpickle
import pathlib


class Application:
    users = {}
    projects = {}
    project = None
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
    def load_projects():
        folder = os.path.join('data', 'projects')
        if not os.path.exists('data'):
            os.mkdir('data')
            Application.projects = None
        elif os.path.exists(folder):
            files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
            for file_name in files:
                with open(os.path.join(folder, file_name), 'rb+') as f:
                    try:
                        project = jsonpickle.decode(f.readline())
                        Application.projects[project.id] = project
                    except Exception:
                        continue

    @staticmethod
    def load_project(project_id):
        folder = os.path.join('data', 'projects')
        if not os.path.exists(folder):
            pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
            Application.project = None
            raise FileNotFoundError('No project with current id')
        elif os.path.exists(os.path.join(folder, str(project_id) + '.json')):
            with open(os.path.join(folder, str(project_id) + '.json'), 'r+') as f:
                try:
                    project = jsonpickle.decode(f.readline())
                    Application.project = project
                except Exception as e:
                    Application.project = None
                    raise e
        else:
            raise FileNotFoundError('No project with current id')

    @staticmethod
    def save_project():
        folder = os.path.join('data', 'projects')
        if not os.path.exists(folder):
            pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
        if Application.project:
            with open(os.path.join(folder, str(Application.project.id) + '.json'), 'w+') as f1, \
                    open(os.path.join(folder, 'last_project.json'), 'w+') as f2:
                try:
                    f1.write(jsonpickle.encode(Application.project))
                    f2.write(jsonpickle.encode(Application.project))
                except Exception as e:
                    Application.project = None
                    raise e

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
    def add_project(project_name):
        Application.project = Project(project_name)

    @staticmethod
    def add_project_task(name, description, tags, parent_id=0, project_id=0):
        if not project_id and not Application.project:
            raise KeyError('Project is not loaded')
        elif not project_id and Application.project or \
                project_id and Application.project and Application.project.id == project_id:
            task = ProjectTask(name=name, description=description, tags=tags, parent_id=parent_id, created_user=Application.cur_user.login)
            Application.project.add_task(task, Application.cur_user.login)
            Application.cur_user.projects.add(project_id)
        elif project_id:
            Application.load_project(project_id)
            if Application.project:
                task = ProjectTask(name=name, description=description, tags=tags, parent_id=parent_id, created_user=Application.cur_user.login)
                Application.project.add_task(task, Application.cur_user.login)
                Application.cur_user.projects.add(project_id)
                # raise exceptions

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
    def complete_project_task(task_id, project_id=0):
        try:
            if project_id:
                Application.load_project(project_id)
            Application.project.complete_task(task_id, Application.cur_user.login)
        except Exception as e:
            raise e

    @staticmethod
    def move_project_task(source_id, destination_id, project_id=0):
        try:
            if project_id:
                Application.load_project(project_id)
            Application.project.move_task(source_id, destination_id)
        except Exception as e:
            raise e

    @staticmethod
    def get_projects():
        folder = os.path.join('data', 'projects')
        projects = []
        if not os.path.exists('data'):
            os.mkdir('data')
            return ''
        elif os.path.exists(folder):
            files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
            for file_name in files:
                if file_name == 'last_project.json':
                    continue
                with open(os.path.join(folder, file_name), 'r+') as f:
                    try:
                        project = jsonpickle.decode(f.readline())
                        projects.append(str(project))
                    except Exception:
                        continue
        return projects

    @staticmethod
    def get_project_users(project_id=0):
        if project_id:
            try:
                Application.load_project(project_id)
            except Exception as e:
                raise e
        users = []
        for user_id in Application.project.users:
            if user_id in Application.users:
                users.append(str(Application.users[user_id]))
        return users

    @staticmethod
    def run():
        Application.load_project('last_project')
        Application.load_users()
