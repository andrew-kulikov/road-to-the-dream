from src import TaskList


class User:
    def __init__(self, login='vasya', password='123', name='vasya'):
        self.login = login
        self._password = password
        self.name = name
        self.task_list = TaskList({})

    def change_password(self, old_password, new_password):
        if old_password == self._password:
            self._password = new_password
        else:
            raise Exception('Wrong password')

    def check_password(self, password):
        return self._password == password

    def add_task(self, task):
        self.task_list.add_task(task)

    def complete_task(self, task_id):
        self.task_list.get_task(task_id).status = 'Completed'


