from .models import TaskList, Task
import jsonpickle


class BasicConnector:

    def __init__(self, tasks_file=None, task_lists_file=None):
        self.__tasks_file = tasks_file
        self.__task_lists_file = task_lists_file

    def save_task(self):
        pass

    def get_task(self):
        pass

    def save_task_list(self):
        pass

    def get_task_list(self):
        pass

    def get_next_task_id(self):
        pass

    def get_next_task_list_id(self):
        pass


class DjangoConnector:

    def __init__(self):
        pass

    def save_task(self):
        pass

    def get_task(self):
        pass

    def save_task_list(self):
        pass

    def get_task_list(self):
        pass

    def get_next_task_id(self):
        pass

    def get_next_task_list_id(self):
        pass
