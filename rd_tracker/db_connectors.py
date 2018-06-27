from rd_tracker.models import TaskList, Task
import jsonpickle
import os


class BasicConnector:

    __DEFAULT_TASKS_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tasks.json')
    __DEFAULT_TASK_LISTS_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'task_lists.json')

    def __init__(self, tasks_file=None, task_lists_file=None):
        self.tasks_file = tasks_file
        if not tasks_file:
            self.tasks_file = self.__DEFAULT_TASKS_FILE
        self.task_lists_file = task_lists_file
        if not task_lists_file:
            self.task_lists_file = self.__DEFAULT_TASK_LISTS_FILE

        if not os.path.exists(self.tasks_file):
            f = open(self.tasks_file, 'w')
            f.close()
        if not os.path.exists(self.task_lists_file):
            f = open(self.task_lists_file, 'w')
            f.close()

    def save_task(self, task):
        if not isinstance(task, Task):
            return TypeError('Given object is not Task')
        with open(self.tasks_file, 'a+') as f:
            f.write(jsonpickle.encode(task) + '\n')

    def get_task(self, task_id):
        tasks = []
        good_task = None
        with open(self.tasks_file, 'r+') as f:
            for line in f:
                task = jsonpickle.decode(line)
                if task.id == task_id:
                    good_task = task
                else:
                    tasks.append(task)

        self.save_tasks(tasks)

        if not good_task:
            raise KeyError('Task with id #{id} does not exist'.format(id=task_id))

        return good_task

    def save_tasks(self, tasks, mode='w'):
        with open(self.tasks_file, mode) as f:
            for task in tasks:
                f.write(jsonpickle.encode(task) + '\n')

    def save_task_list(self, task_list):
        if not isinstance(task_list, TaskList):
            return TypeError('Given object is not TaskList')
        with open(self.task_lists_file, 'a+') as f:
            f.write(jsonpickle.encode(task_list) + '\n')

    def get_task_list(self, task_list_id):
        task_lists = []
        good_task_list = None
        with open(self.task_lists_file, 'r+') as f:
            for line in f:
                task_list = jsonpickle.decode(line)
                if task_list.id == task_list_id:
                    good_task_list = task_list
                else:
                    task_lists.append(task_list)

        self.save_task_lists(task_lists)

        if not good_task_list:
            raise KeyError('Task list with id #{id} does not exist'.format(id=task_list_id))

        return good_task_list

    def save_task_lists(self, task_lists, mode='w'):
        with open(self.task_lists_file, mode) as f:
            for task_list in task_lists:
                f.write(jsonpickle.encode(task_list) + '\n')

    def get_next_task_id(self):
        next_id = 0
        with open(self.tasks_file, 'r+') as f:
            for line in f:
                task = jsonpickle.decode(line)
                next_id = max(next_id, task.id + 1)
        return next_id

    def get_next_task_list_id(self):
        next_id = 0
        with open(self.task_lists_file, 'r+') as f:
            for line in f:
                task_list = jsonpickle.decode(line)
                next_id = max(next_id, task_list.id + 1)
        return next_id

    def get_user_task_lists(self, user_id):
        user_lists = []
        other_lists = []
        with open(self.task_lists_file, 'r+') as f:
            for line in f:
                task_list = jsonpickle.decode(line)
                if not task_list.users or user_id not in task_list.users:
                    other_lists.append(task_list)
                    continue
                user_lists.append(task_list)

        self.save_tasks(other_lists)

        return user_lists

    def get_subtasks(self, task_id):
        subtasks = []
        other_tasks = []
        with open(self.tasks_file, 'r+') as f:
            for line in f:
                task = jsonpickle.decode(line)
                if task.parent_id and task.parent_id == task_id:
                    subtasks.append(task)
                else:
                    other_tasks.append(task)

        self.save_tasks(other_tasks)

        return subtasks

    def get_task_list_tasks(self, task_list_id):
        task_list_tasks = []
        other_tasks = []
        with open(self.tasks_file, 'r+') as f:
            for line in f:
                task = jsonpickle.decode(line)
                if task.task_list == task_list_id:
                    task_list_tasks.append(task)
                else:
                    other_tasks.append(task)

        self.save_tasks(other_tasks)

        return task_list_tasks

    def get_all_tasks(self):
        root_tasks = []
        other_tasks = []
        with open(self.tasks_file, 'r+') as f:
            for line in f:
                task = jsonpickle.decode(line)
                if not task.parent_id:
                    root_tasks.append(task)
                else:
                    other_tasks.append(task)

        self.save_tasks(other_tasks)

        return root_tasks

    def get_user_tasks(self):
        pass

    def get_all_users(self):
        users = set()
        with open(self.tasks_file, 'r+') as f:
            for line in f:
                task = jsonpickle.decode(line)
                if task.created_user:
                    users.add(task.created_user)
                if task.completed_user:
                    users.add(task.completed_user)

        return users
