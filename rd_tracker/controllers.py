"""controllers module
Designed to give basic interface to interact with Task and TaskList.
Contains Controller class that implements those basic methods.

All methods have similar structure:
1. Gets object from database.
2. Applies some changes or filter data according given rules.
3. Raises exceptions if given data or queries is not valid.
4. Saves changed data in database and returns it.

Database communication interface is represented by __connector.

Public methods
    'add_task': adds task in database via connector.
    'delete_task': remove task with all subtasks from database.
    'add_task_list: adds task list in database.
    'delete_task_list': removes task list from database with all tasks.
    'get_subtaks': get all subtasks that have parent_id equals to given task_id.
    'get_all_tasks': get all tasks in database.
    'get_task': get task with given id from database.
    'complete_task': complete task with given id.
    'edit_task': change task parameters.
    'edit_task_list': change task list parameters.
    'invite_user': add user in task list with given id.
    'get_user_task_lists': get all task lists that user participate in.
    'get_task_list_tasks': get all tasks in given task list.
    'change_connector': change self.__connector by new connector.
    'add_task_list_user': add user in task list with given id.
    'sort_tasks': sort tasks by given parameter (name, deadline, priority).
    'get_all_users': get all users that at least once created or completed task.
"""

from rd_tracker.models import Task, TaskList
from rd_tracker.db_connectors import BasicConnector


class Controller:

    def __init__(self, connector=None):
        if not connector:
            self.__connector = BasicConnector()
        elif not isinstance(connector, BasicConnector):
            raise TypeError('Given object is not BasicConnector')
        else:
            self.__connector = connector

    def add_task(self, task):
        """Validates given tasks and adds to the database.

        :param task: task object to add in database.
        :return: id of saved task.
        :raises
        'TypeError': if given object is not task.
        'Exception': if task's task list is not the same as parent task list.
        """
        if not isinstance(task, Task):
            raise TypeError('Given object is not Task')

        next_id = self.__connector.get_next_task_id()
        task.id = next_id

        if task.parent_id:
            parent = self.__connector.get_task(task.parent_id)
            if not task.task_list:
                task.task_list = parent.task_list
            if parent.task_list != task.task_list:
                self.__connector.save_task(parent)
                self.__connector.save_task(task)
                raise Exception('Tasks must be in one task list')
            # user in task list
            self.__connector.save_task(parent)

        self.__connector.save_task(task)
        return task.id

    def delete_task(self, task_id):
        """Remove task with all subtasks from database.

        :param task_id: id of task to be removed.
        :return: None
        :raises
        'TypeError': if task_id is not int.
        """
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
        """Add task list in database.

        :param task_list: task list object to be added in database.
        :return: id of saved task list.
        :raises
        'TypeError': if given object is not TaskList instance.
        """
        if not isinstance(task_list, TaskList):
            raise TypeError('Given object is not TaskList')

        task_list.id = self.__connector.get_next_task_list_id()

        self.__connector.save_task_list(task_list)
        return task_list.id

    def delete_task_list(self, task_list_id):
        task_list = self.__connector.get_task_list(task_list_id)
        tasks = self.get_task_list_tasks(task_list.id)
        for task in tasks:
            self.delete_task(task.id)

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
        task_list = self.__connector.get_task_list(task_list_id)
        if 'name' in attrs:
            if not isinstance(attrs['name'], str):
                self.__connector.save_task_list(task_list)
                raise AttributeError('Given task list name is not not string')
            task_list.name = attrs['name']

        if 'is_private':
            if not isinstance(attrs['is_private'], bool):
                self.__connector.save_task_list(task_list)
                raise AttributeError('Given task list privacy is not not bool')
            task_list.is_private = attrs['is_private']
            if task_list.is_private:
                task_list.users.clear()
                task_list.users.add(task_list.created_user)

        self.__connector.save_task_list(task_list)

    def invite_user(self, task_list_id, user_id):
        task_list = self.__connector.get_task_list(task_list_id)
        task_list.users.add(user_id)
        self.__connector.save_task_list(task_list)

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
