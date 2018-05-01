from src import TaskList
import random


class User:
    def __init__(self, login='vasya', password='123', name='vasya'):
        self.id = random.randint(0, 1000)
        self.login = login
        self._password = password
        self.name = name
        self.pending_tasks = TaskList({})
        self.completed_tasks = TaskList({})

    def change_password(self, old_password, new_password):
        if old_password == self._password:
            self._password = new_password
        else:
            raise Exception('Wrong password')

    def check_password(self, password):
        return self._password == password

    def add_task(self, task):
        self.pending_tasks.add_task(task)
        if task.parent_id:
            self.pending_tasks.add_child(task.id, task.parent_id)

    def complete_task(self, task_id):
        task_to_complete = self.pending_tasks.get_task(task_id)
        self.completed_tasks.add_task(task_to_complete)
        self.pending_tasks.remove_task(task_id)
        try:
            tasks = task_to_complete.sub_tasks
        except KeyError as e:
            raise e
        except AttributeError as e:
            raise e
        if not tasks:
            return
        for task in tasks:
            self.complete_task(task)

    def __str__(self):
        return self.login + ' (' + self.name + ')'
