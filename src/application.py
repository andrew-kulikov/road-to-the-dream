from src import TaskList, User, Task, Project, ProjectTask
import os
import json
import jsonpickle
import pathlib
import datetime


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
        with open(os.path.join('data', 'users.json'), 'w+') as f:
            f.write(jsonpickle.encode(Application.users))
        with open(os.path.join('data', 'cur_user.txt'), 'w', encoding='utf-8') as f:
            if Application.cur_user:
                f.write(Application.cur_user.login)

    @staticmethod
    def load_users():
        if not os.path.exists('data\\'):
            os.mkdir('data\\')
            Application.users = None
        elif os.path.exists(os.path.join('data', 'users.json')):
            with open(os.path.join('data', 'users.json'), 'r+') as f:
                Application.users = jsonpickle.decode(f.readline())
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
    def add_task(name, description, tags, priority=0, parent_id=0, deadline=None, period=None):
        if not Application.cur_user:
            raise AttributeError('You are not logged in')
        task = Task(name=name, description=description, tags=tags, period=period,
                    parent_id=parent_id, priority=priority, end_date=deadline)
        Application.cur_user.add_task(task)

    @staticmethod
    def edit_task(task_id, name, description, tags,
                  priority=0, deadline=None, period=None):
        if not Application.cur_user:
            raise AttributeError('You are not logged in')
        Application.cur_user.edit_task(task_id=task_id, name=name, description=description, tags=tags,
                                       priority=priority, deadline=deadline, period=period)

    @staticmethod
    def add_project(project_name):
        Application.project = Project(project_name)

    @staticmethod
    def add_project_task(name, description, tags, parent_id=0, project_id=0, priority=0, deadline=None, period=None):
        if not project_id and not Application.project:
            raise KeyError('Project is not loaded')
        elif not project_id and Application.project or \
                project_id and Application.project and Application.project.id == project_id:
            task = ProjectTask(name=name, description=description, tags=tags,
                               parent_id=parent_id, created_user=Application.cur_user.login,
                               priority=priority, end_date=deadline, period=period)
            Application.project.add_task(task, Application.cur_user.login)
            Application.cur_user.projects.add(project_id)
        elif project_id:
            Application.load_project(project_id)
            if Application.project:
                task = ProjectTask(name=name, description=description, tags=tags,
                                   parent_id=parent_id, created_user=Application.cur_user.login,
                                   priority=priority, end_date=deadline, period=period)
                Application.project.add_task(task, Application.cur_user.login)
                Application.cur_user.projects.add(project_id)
                # raise exceptions

    @staticmethod
    def edit_project_task(task_id, name, description, tags,
                          project_id=0, priority=0, deadline=None, period=None):
        if project_id:
            Application.load_project(project_id)
        Application.project.edit_task(task_id=task_id, name=name, description=description, tags=tags,
                                      priority=priority, deadline=deadline, period=period)

    @staticmethod
    def get_task_list(list_type='pending'):
        if not Application.cur_user:
            raise AttributeError('You are not logged in')
        if list_type == 'pending':
            return Application.cur_user.pending_tasks.print_list()
        elif list_type == 'completed':
            return Application.cur_user.completed_tasks.print_list()
        elif list_type == 'failed':
            return Application.cur_user.failed_tasks.print_list()

    @staticmethod
    def get_project_task_list(list_type='pending', project_id=0):
        if project_id:
            Application.load_project(project_id)
        if list_type == 'pending':
            return Application.project.pending_tasks.print_list()
        elif list_type == 'completed':
            return Application.project.completed_tasks.print_list()
        elif list_type == 'failed':
            return Application.project.failed_tasks.print_list()

    @staticmethod
    def complete_task(task_id):
        if not Application.cur_user:
            raise AttributeError('You are not logged in')
        Application.cur_user.complete_task(task_id)

    @staticmethod
    def move_task(source_id, destination_id):
        if not Application.cur_user:
            raise AttributeError('You are not logged in')
        Application.cur_user.move_task(source_id, destination_id)

    @staticmethod
    def remove_task(task_id):
        if not Application.cur_user:
            raise AttributeError('You are not logged in')
        Application.cur_user.remove_task(task_id)

    @staticmethod
    def remove_project_task(task_id, project_id=0):
        if project_id:
            Application.load_project(project_id)
        if not Application.project:
            raise AttributeError('Project is not loaded')
        Application.project.remove_task(task_id)

    @staticmethod
    def complete_project_task(task_id, project_id=0):
        if project_id:
            Application.load_project(project_id)
        if not Application.project:
            raise AttributeError('Project is not loaded')
        Application.project.complete_task(task_id, Application.cur_user.login)

    @staticmethod
    def move_project_task(source_id, destination_id, project_id=0):
        if project_id:
            Application.load_project(project_id)
        if not Application.project:
            raise AttributeError('Project is not loaded')
        Application.project.move_task(source_id, destination_id)

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
            Application.load_project(project_id)
        if not Application.project:
            raise AttributeError('Project is not loaded')
        users = []
        removed_users = []
        for user_id in Application.project.users:
            if user_id in Application.users:
                users.append(str(Application.users[user_id]))
            else:
                removed_users.append(user_id)
        for user_id in removed_users:
            Application.project.users.remove(user_id)
        return users

    @staticmethod
    def sort_user_tasks(sort_type):
        if not Application.cur_user:
            raise AttributeError('You are not logged in')
        sorts = {
            'name': lambda task: task.name,
            'date': lambda task: task.date,
            'priority': lambda task: task.priority}
        if sort_type in sorts:
            Application.cur_user.pending_tasks.sort_by(sorts[sort_type])
        else:
            raise KeyError('No such sort type')

    @staticmethod
    def sort_project_tasks(sort_type, project_id=0):
        if project_id:
            Application.load_project(project_id)
        if not Application.project:
            raise AttributeError('Project is not loaded')
        sorts = {
            'name': lambda task: task.name,
            'date': lambda task: task.date if task.date else datetime.datetime(year=2900, month=1, day=5),
            'priority': lambda task: task.priority
        }
        if sort_type in sorts:
            Application.project.pending_tasks.sort_by(sorts[sort_type])
        else:
            raise KeyError('No such sort type')

    @staticmethod
    def run():
        try:
            Application.load_users()
            Application.load_project('last_project')
        finally:
            if Application.cur_user:
                Application.cur_user.update_tasks()

