from src.models import Task, TaskList
from src.db_connectors import BasicConnector


class Controller:

    def __init__(self, connector=None):
        if not connector:
            self.__connector = BasicConnector()
        elif not isinstance(connector, BasicConnector):
            raise TypeError('Given object is not BasicConnector')
        else:
            self.__connector = connector

    def add_task(self, task, user_id=None):

        if not isinstance(task, Task):
            raise TypeError('Given object is not Task')

        next_id = self.__connector.get_next_task_id()
        task.id = next_id

        task.created_user = user_id

        if task.parent_id:
            parent = self.__connector.get_task(task.parent_id)
            if not task.task_list:
                task.task_list = parent.task_list
            if parent.tast_list != task.task_list:
                self.__connector.save_task(parent)
                raise Exception('Tasks must be in one task list')
            # user in task list
            self.__connector.save_task(parent)

        self.__connector.save_task(task)

    def delete_task(self, task_id):

        if not isinstance(task_id, int):
            raise TypeError('Task id is not int')

        task = self.__connector.get_task(task_id)

        def delete_subtasks(task_id):
            subtasks = self.__connector.get_subtasks(task_id)
            if not subtasks or not len(subtasks):
                return
            for subtask in subtasks:
                delete_subtasks(subtask.id)

        delete_subtasks(task.id)

    def add_task_list(self, task_list):
        if not isinstance(task_list, TaskList):
            raise TypeError('Given object is not TaskList')

        task_list.id = self.__connector.get_next_task_list_id()

        self.__connector.save_task_list(task_list)

    def delete_task_list(self, task_list_id):
        task_list = self.__connector.get_task_list(task_list_id)

    def get_subtasks(self, task_id):
        tasks = self.__connector.get_subtasks(task_id)
        self.__connector.save_tasks(tasks, 'a+')
        return tasks

    def get_all_tasks(self):
        tasks = self.__connector.get_all_tasks()
        self.__connector.save_tasks(tasks, 'a+')
        return tasks

    def get_task(self, task_id):
        task = self.__connector.get_task(task_id)
        self.__connector.save_task(task)
        return task

    def complete_task(self, task_id):
        task = self.__connector.get_task(task_id)
        self.__connector.save_task(task)

        def complete_subtasks(task_id):
            subtasks = self.__connector.get_subtasks(task_id)
            if not subtasks or not len(subtasks):
                return
            for subtask in subtasks:
                subtask.status = 'C'
                self.__connector.save_task(subtask)
                complete_subtasks(subtask.id)

        complete_subtasks(task.id)

    def edit_task(self, task_id, attrs):
        pass

    def edit_task_list(self, task_list_id, attrs):
        pass

    def invite_user(self, task_list_id, user_id):
        pass

    def get_user_task_lists(self, user_id):
        lists = self.__connector.get_user_task_lists(user_id)
        self.__connector.save_task_lists(lists, 'a+')
        return lists

    def get_task_list_tasks(self, task_list_id):
        tasks = self.__connector.get_task_list_tasks(task_list_id)
        self.__connector.save_tasks(tasks, 'a+')
        return tasks

    def change_connector(self, connector):
        self.__connector = connector

    def add_task_list_user(self, task_list_id, user_id):
        task_list = self.__connector.get_task_list(task_list_id)
        task_list.users.append(user_id)
        self.__connector.save_task_list(task_list)

    def sort_tasks(self, sort_type):
        sorts = {
            'title': lambda task: task.title,
            'deadline': lambda task: task.deadline,
            'priority': lambda task: task.priority}
        if sort_type not in sorts:
            # self.logger.error('Cannot sort with parameter ' + str(sort_type))
            raise KeyError('No such sort type')
        tasks = self.__connector.get_all_tasks()
        tasks.sort(key=sorts[sort_type])
        self.__connector.save_tasks(tasks, 'a+')

        def sort_subtasks(task_id):
            subtasks = self.__connector.get_subtasks(task_id)
            if not subtasks or not len(subtasks):
                return
            subtasks.sort(key=sorts[sort_type])
            self.__connector.save_tasks(subtasks, 'a+')
            for subtask in subtasks:
                sort_subtasks(subtask.id)

        for task in tasks:
            sort_subtasks(task)

        # self.logger.info('Tasks sorted by ' + str(sort_type))

        return tasks

    def get_all_users(self):
        return self.__connector.get_all_users()
