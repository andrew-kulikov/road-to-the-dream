from src import TaskList, User, Task, Project, ProjectTask
from src.tools import parsers
import os
import jsonpickle
import pathlib
import datetime
import logging


class Application:
    def __init__(self, config_path=os.path.join('..', '..', 'config', 'config.ini'), database_folder=None,
                 users_file=None, cur_user_file=None, projects_folder=None, log_file=None):
        self.users = {}
        self.project = None
        self.cur_user = None
        try:
            config = parsers.parse_config(config_path)
        except Exception:
            config = None
        default = None
        if config:
            default = config['DEFAULT']

        if database_folder:
            self.database_folder = database_folder
        elif default:
            self.database_folder = default['database_folder']
        else:
            self.database_folder = 'data'

        if projects_folder:
            self.projects_folder = projects_folder
        elif default:
            self.projects_folder = default['projects_folder']
        else:
            self.projects_folder = 'projects'

        if users_file:
            self.users_file = users_file
        elif default:
            self.users_file = default['users_file']
        else:
            self.users_file = 'users.json'

        if cur_user_file:
            self.cur_user_file = cur_user_file
        elif default:
            self.cur_user_file = default['cur_user_file']
        else:
            self.cur_user_file = 'cur_user.txt'

        if log_file:
            self.log_file = log_file
        elif default:
            self.log_file = default['log_file']
        else:
            self.log_file = 'log.log'

        self.logger = self._get_logger()

        try:
            self.load_users()
            self.load_project('last_project')
        finally:
            if self.cur_user:
                self.cur_user.update_tasks()

    def _get_logger(self):
        logger = logging.getLogger('spam_application')
        logger.setLevel(logging.INFO)
        logger.setLevel(logging.ERROR)
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(self.log_file)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(fh)
        return logger

    def authorize(self, login, password):
        if login in self.users:
            if self.users[login].check_password(password):
                self.cur_user = self.users[login]
                self.logger.info('Authorized as user {user}'.format(user=str(self.cur_user)))
            else:
                self.logger.error('Wrong password for user {user}'.format(user=login))
                raise KeyError('Wrong password')
        else:
            self.logger.error('User {user} does not exist'.format(user=login))
            raise KeyError('User does not exist')

    def register_user(self, name, login, password):
        if self.users.get(login, None):
            self.logger.error('User {user} already exists'.format(user=login))
            raise KeyError('User with this login already exists')
        new_user = User(login, password, name)
        self.users[login] = new_user
        self.cur_user = new_user
        self.logger.info('User {user} registered'.format(user=str(self.cur_user)))

    def save_users(self):
        if not os.path.exists(self.database_folder):
            os.mkdir(self.database_folder)
        with open(os.path.join(self.database_folder, self.users_file), 'w+') as f:
            f.write(jsonpickle.encode(self.users))
        with open(os.path.join(self.database_folder, self.cur_user_file), 'w', encoding='utf-8') as f:
            if self.cur_user:
                f.write(self.cur_user.login)
        self.logger.debug('Users saved')

    def load_users(self):
        if not os.path.exists(self.database_folder):
            os.mkdir(self.database_folder)
            self.users = None
        elif os.path.exists(os.path.join(self.database_folder, self.users_file)):
            with open(os.path.join(self.database_folder, self.users_file), 'r') as f:
                self.users = jsonpickle.decode(f.readline())
        self.load_cur_user()
        self.logger.debug('Users loaded')

    def load_project(self, project_id):
        folder = os.path.join(self.database_folder, self.projects_folder)
        if not os.path.exists(folder):
            pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
            self.project = None
            self.logger.error('No project with id #{id}'.format(id=project_id))
            raise FileNotFoundError('No project with current id')
        elif os.path.exists(os.path.join(folder, str(project_id) + '.json')):
            with open(os.path.join(folder, str(project_id) + '.json'), 'r') as f:
                try:
                    project = jsonpickle.decode(f.readline())
                    self.project = project
                    self.logger.debug('Project #{id} loaded'.format(id=project_id))
                except Exception as e:
                    self.project = None
                    self.logger.error('Bad project file')
                    raise e
        else:
            self.logger.error('No project with id #{id}'.format(id=project_id))
            raise FileNotFoundError('No project with current id')

    def save_project(self):
        folder = os.path.join(self.database_folder, self.projects_folder)
        if not os.path.exists(folder):
            pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
        if self.project:
            with open(os.path.join(folder, str(self.project.id) + '.json'), 'w+') as f1, \
                    open(os.path.join(folder, 'last_project.json'), 'w+') as f2:
                try:
                    f1.write(jsonpickle.encode(self.project))
                    f2.write(jsonpickle.encode(self.project))
                    self.logger.debug('Project #{id} saved'.format(id=self.project.id))
                except Exception as e:
                    self.project = None
                    self.logger.error('Bad file, project #{id} cannot be saved'.format(id=self.project.id))
                    raise e

    def load_cur_user(self):
        if not os.path.exists(os.path.join(self.database_folder, self.cur_user_file)):
            open(os.path.join(self.database_folder, self.cur_user_file), 'w').close()
            self.cur_user = None
        else:
            with open(os.path.join(self.database_folder, self.cur_user_file), 'r', encoding='utf-8') as f:
                try:
                    login = f.readline().strip()
                    self.cur_user = self.users[login]
                except KeyError:
                    self.cur_user = None
                    self.logger.error('No user with login #{id}'.format(id=login))

    def add_task(self, name, description, tags, priority=0, parent_id=0, deadline=None, period=None):
        if not self.cur_user:
            self.logger.error('Cannot add task: there is no authorized user.')
            raise AttributeError('You are not logged in')
        task = Task(name=name, description=description, tags=tags, period=period,
                    parent_id=parent_id, priority=priority, end_date=deadline)
        self.cur_user.add_task(task)
        self.logger.info('Added task #{id}'.format(id=task.id))

    def edit_task(self, task_id, name, description, tags,
                  priority=0, deadline=None, period=None):
        if not self.cur_user:
            self.logger.error('Cannot edit task: there is no authorized user.')
            raise AttributeError('You are not logged in')
        self.cur_user.edit_task(task_id=task_id, name=name, description=description, tags=tags,
                                priority=priority, deadline=deadline, period=period)
        self.logger.info('Edited task #{id}'.format(id=task_id))

    def get_full_task_info(self, task_id):
        try:
            s = self.cur_user.get_full_task_info(task_id)
            self.logger.info('Got full info of task #{id}'.format(id=task_id))
        except KeyError as e:
            self.logger.error('Task with id #{id} does not exist'.format(id=task_id))
            s = ''
            raise e
        return s

    def add_project(self, project_name):
        self.project = Project(project_name)
        self.logger.info('Added project #{id}'.format(id=self.project.id))

    def add_project_task(self, name, description, tags, parent_id=0, project_id=0,
                         priority=0, deadline=None, period=None):
        if not project_id and not self.project:
            self.logger.error('Cannot add task: there is no loaded project.')
            raise KeyError('Project is not loaded')
        if project_id:
            self.load_project(project_id)
        if self.project:
            task = ProjectTask(name=name, description=description, tags=tags,
                               parent_id=parent_id, created_user=self.cur_user.login,
                               priority=priority, end_date=deadline, period=period)
            self.project.add_task(task, self.cur_user.login)
            self.cur_user.projects.add(project_id)

    def edit_project_task(self, task_id, name, description, tags,
                          project_id=0, priority=0, deadline=None, period=None):
        if project_id:
            self.load_project(project_id)
        self.project.edit_task(task_id=task_id, name=name, description=description, tags=tags,
                               priority=priority, deadline=deadline, period=period)

    def get_task_list(self, list_type='pending'):
        if not self.cur_user:
            self.logger.error('Cannot get task list: there is no authorized user.')
            raise AttributeError('You are not logged in')
        s = None
        if list_type == 'pending':
            s = self.cur_user.pending_tasks.print_list()
        elif list_type == 'completed':
            s = self.cur_user.completed_tasks.print_list()
        elif list_type == 'failed':
            s = self.cur_user.failed_tasks.print_list()
        if s:
            self.logger.info('Got {type} task list'.format(type=list_type))
        return s

    def get_project_task_list(self, list_type='pending', project_id=0):
        if project_id:
            self.load_project(project_id)
        if list_type == 'pending':
            return self.project.pending_tasks.print_list()
        elif list_type == 'completed':
            return self.project.completed_tasks.print_list()
        elif list_type == 'failed':
            return self.project.failed_tasks.print_list()

    def complete_task(self, task_id):
        if not self.cur_user:
            self.logger.error('Cannot complete task: there is no authorized user.')
            raise AttributeError('You are not logged in')
        self.cur_user.complete_task(task_id)
        self.logger.info('Task #{id} completed'.format(id=task_id))

    def move_task(self, source_id, destination_id):
        if not self.cur_user:
            self.logger.error('Cannot move task: there is no authorized user.')
            raise AttributeError('You are not logged in')
        self.cur_user.move_task(source_id, destination_id)
        self.logger.info('Task #{source_id} moved to sub tasks of #{dest}'.format(source_id=source_id,
                                                                                  dest=destination_id))

    def remove_task(self, task_id):
        if not self.cur_user:
            self.logger.error('Cannot remove task: there is no authorized user.')
            raise AttributeError('You are not logged in')
        self.cur_user.remove_task(task_id)
        self.logger.info('Task #{id} removed'.format(id=task_id))

    def remove_project_task(self, task_id, project_id=0):
        if project_id:
            self.load_project(project_id)
        if not self.project:
            self.logger.error('Cannot remove task: there is no loaded project.')
            raise AttributeError('Project is not loaded')
        self.project.remove_task(task_id)
        self.logger.info('Task #{id} removed'.format(id=task_id))

    def complete_project_task(self, task_id, project_id=0):
        if project_id:
            self.load_project(project_id)
        if not self.project:
            self.logger.error('Cannot complete task: there is no loaded project.')
            raise AttributeError('Project is not loaded')
        self.project.complete_task(task_id, self.cur_user.login)
        self.logger.info('Task #{id} completed'.format(id=task_id))

    def move_project_task(self, source_id, destination_id, project_id=0):
        if project_id:
            self.load_project(project_id)
        if not self.project:
            self.logger.error('Cannot move task: there is no loaded project.')
            raise AttributeError('Project is not loaded')
        self.project.move_task(source_id, destination_id)
        self.logger.info('Task #{source_id} moved to sub tasks of #{dest}'.format(source_id=source_id,
                                                                                  dest=destination_id))

    def get_projects(self):
        folder = os.path.join(self.database_folder, 'projects')
        projects = []
        if not os.path.exists(self.database_folder):
            os.mkdir(self.database_folder)
            return ''
        elif os.path.exists(folder):
            files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
            for file_name in files:
                if file_name == 'last_project.json':
                    continue
                with open(os.path.join(folder, file_name), 'r') as f:
                    try:
                        project = jsonpickle.decode(f.readline())
                        projects.append(str(project))
                    except:
                        continue
        return projects

    def get_project_users(self, project_id=0):
        if project_id:
            self.load_project(project_id)
        if not self.project:
            raise AttributeError('Project is not loaded')
        users = []
        removed_users = []
        for user_id in self.project.users:
            if user_id in self.users:
                users.append(str(self.users[user_id]))
            else:
                removed_users.append(user_id)
        for user_id in removed_users:
            self.project.users.remove(user_id)
        return users

    def sort_user_tasks(self, sort_type):
        if not self.cur_user:
            raise AttributeError('You are not logged in')
        sorts = {
            'name': lambda task: task.name,
            'deadline': lambda task: task.date,
            'priority': lambda task: task.priority}
        if sort_type in sorts:
            self.cur_user.pending_tasks.sort_by(sorts[sort_type])
            self.logger.info('Tasks sorted by ' + str(sort_type))
        else:
            self.logger.error('Cannot sort with parameter ' + str(sort_type))
            raise KeyError('No such sort type')

    def sort_project_tasks(self, sort_type, project_id=0):
        if project_id:
            self.load_project(project_id)
        if not self.project:
            raise AttributeError('Project is not loaded')
        sorts = {
            'name': lambda task: task.name,
            'deadline': lambda task: task.date if task.date else datetime.datetime(year=2900, month=1, day=5),
            'priority': lambda task: task.priority
        }
        if sort_type in sorts:
            self.project.pending_tasks.sort_by(sorts[sort_type])
            self.logger.info('Tasks sorted by ' + str(sort_type))
        else:
            self.logger.error('Cannot sort with parameter ' + str(sort_type))
            raise KeyError('No such sort type')
