from .models import TaskList, Task
import jsonpickle
import os


class BasicConnector:

    __DEFAULT_TASKS_FILE = os.path.dirname(os.path.realpath(__file__)) + '/tasks.json'
    __DEFAULT_TASK_LISTS_FILE = os.path.dirname(os.path.realpath(__file__)) + '/task_lists.json'

    def __init__(self, tasks_file=None, task_lists_file=None):
        self.tasks_file = tasks_file
        if not tasks_file:
            self.tasks_file = self.__DEFAULT_TASKS_FILE
        self.task_lists_file = task_lists_file
        if not task_lists_file:
            self.task_lists_file = self.__DEFAULT_TASK_LISTS_FILE

    def save_task(self, task):
        if not isinstance(task, Task):
            return TypeError('Given object is not Task')
        with open(self.tasks_file, 'a+') as f:
            f.write(jsonpickle.encode(task))

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

    def save_tasks(self, tasks):
        with open(self.tasks_file, 'w') as f:
            for task in tasks:
                f.write(jsonpickle.encode(task))

    def save_task_list(self, task_list):
        if not isinstance(task_list, TaskList):
            return TypeError('Given object is not TaskList')
        with open(self.tasks_file, 'a+') as f:
            f.write(jsonpickle.encode(task_list))

    def get_task_list(self, task_list_id):
        tasks = []
        good_task_list = None
        with open(self.task_lists_file, 'r+') as f:
            for line in f:
                task_list = jsonpickle.decode(line)
                if task_list.id == task_list_id:
                    good_task_list = task_list
                else:
                    tasks.append(task_list)

        self.save_tasks(tasks)

        if not good_task_list:
            raise KeyError('Task list with id #{id} does not exist'.format(id=task_list_id))

        return good_task_list

    def save_task_lists(self, task_lists):
        with open(self.task_lists_file, 'w') as f:
            for task_list in task_lists:
                f.write(jsonpickle.encode(task_list))

    def get_next_task_id(self):
        next_id = 0
        with open(self.tasks_file, 'r+') as f:
            for line in f:
                task = jsonpickle.decode(line)
                if task.id != next_id:
                    break
                next_id += 1
        return next_id

    def get_next_task_list_id(self):
        next_id = 0
        with open(self.task_lists_file, 'r+') as f:
            for line in f:
                task_list = jsonpickle.decode(line)
                if task_list.id != next_id:
                    break
                next_id += 1
        return next_id
