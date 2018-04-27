from src import TaskList


class User:
    def __init__(self):
        self.login = 'vasya'
        self.password = '123'
        self.name = 'vasya'
        self.passphrase = ''
        self.task_list = TaskList([])
        self.id = 'sdfsdfsdfsdf'

    def change_password(self, old_password, new_password):
        if old_password == self.password:
            self.password = new_password
        else:
            raise Exception('Wrong password')

    def add_task(self):
        pass
