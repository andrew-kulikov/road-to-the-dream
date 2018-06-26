from .models import Task, TaskList
from .db_connectors import BasicConnector


class Controller:

    def __init__(self, connector=None):
        if not isinstance(connector, BasicConnector):
            raise TypeError('Given object is not BasicConnector')
        self.__connector = connector

    def add_task(self, task, user_id=None):

        if not isinstance(task, Task):
            raise TypeError('Given object is not Task')

        next_id = self.__connector.get_next_task_id()
        task.id = next_id

        task.created_user = user_id

        if task.parent_id:
            parent = self.__connector.get_task(task.parent_id)
            if parent.tast_list != task.task_list:
                self.__connector.save_task(parent)
                raise Exception('Tasks must be in one task list')
            # user in task list
            self.__connector.save_task(parent)

        self.__connector.save_task(task)

    def delete_task(self):
        pass

    def add_task_list(self):
        pass

    def delete_task_list(self):
        pass

    def get_sub_tasks(self):
        pass

    def get_all_tasks(self):
        pass

    def add_sub_task(self):
        pass

    def get_task(self):
        pass

    def edit_task(self):
        pass

    def edit_task_list(self):
        pass

    def invite_user(self):
        pass

    def get_user_task_lists(self):
        pass

    def get_task_list_tasks(self):
        pass

    def change_connector(self):
        pass

