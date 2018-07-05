"""db_connectors module

This module contains classes that implements interface to communicate with databases.

Public classes:

'BasicConnector': designed to provide communication with simple file database.
"""

import os

import jsonpickle

from rd_tracker.models import TaskList, Task


class BasicConnector:
    """
    Class that provides communication with simple database built on json files.

    Attributes:
        tasks_file(str): path to file with tasks.
        task_lists_file(str):  path to file with task lists.

    Public methods:
        save_task: save task into the file.
        get_task: take task out of the file.
        save_tasks: save all tasks into the file.
        save_task_list: save task list into the file.
        get_task_list: take task list from the file.
        save_task_lists: save all task lists into the file.
        get_next_task_id: return free task id.
        get_next_task_list_id: return free task list id.
        get_user_task_lists: return all task lists of given user.
        get_subtasks: get all subtasks of given task.
        get_task_list_tasks: get all tasks in given taks list.
        get_all_tasks: get all tasks in database.
        get_user_tasks: get all tasks of given user.
        get_all_users: get all users in database.


    """

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
        """Save given task in tasks file.

        Task will be converted into json format and appended to the file.

        :param task: task to save.
        :return:
        :raises
        'TypeError': if given object is not `Task`.
        """
        if not isinstance(task, Task):
            return TypeError('Given object is not Task')
        with open(self.tasks_file, 'a+') as f:
            f.write(jsonpickle.encode(task) + '\n')

    def get_task(self, task_id):
        """Get task with given id from file.

        :param task_id: id of task to pick from file.
        :return: task with given id.
        :raises
        'KeyError': if task was not found in database.
        """
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
        """Save all tasks in given list to file.

        :param tasks: list of tasks (each task should have type `Task`)
        :param mode: if mode == 'a', tasks will be appended to the file,
        if mode == 'w', tasks file will be overwritten.
        :return:
        """
        with open(self.tasks_file, mode) as f:
            for task in tasks:
                f.write(jsonpickle.encode(task) + '\n')

    def save_task_list(self, task_list):
        """Save given task list in task_lists file.

        Task list will be converted into json format and appended to the file.

        :param task_list: task list to save.
        :return:
        :raises
        'TypeError': if given object is not `TaskList`.
        """
        if not isinstance(task_list, TaskList):
            return TypeError('Given object is not TaskList')
        with open(self.task_lists_file, 'a+') as f:
            f.write(jsonpickle.encode(task_list) + '\n')

    def get_task_list(self, task_list_id):
        """Get task list with given id from file.

        :param task_list_id: id of task list to pick from file.
        :return: task list with given id.
        :raises
        'KeyError': if task list was not found in database.
        """
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
        """Save all task lists in given list to file.

        :param task_lists: list of task lists (each element should have type `TaskList`)
        :param mode: if mode == 'a', task lists will be appended to the file,
        if mode == 'w', task_lists file will be overwritten.
        :return:
        """
        with open(self.task_lists_file, mode) as f:
            for task_list in task_lists:
                f.write(jsonpickle.encode(task_list) + '\n')

    def get_next_task_id(self):
        """Free task id.

        This function takes maximum task id from db and returns max_id + 1.

        :return: `int` free task id.
        """
        next_id = 0
        with open(self.tasks_file, 'r+') as f:
            for line in f:
                task = jsonpickle.decode(line)
                next_id = max(next_id, task.id + 1)
        return next_id

    def get_next_task_list_id(self):
        """Free task id.

        This function takes maximum task list id from db and returns max_id + 1.

        :return: `int` free task list id.
        """
        next_id = 0
        with open(self.task_lists_file, 'r+') as f:
            for line in f:
                task_list = jsonpickle.decode(line)
                next_id = max(next_id, task_list.id + 1)
        return next_id

    def get_user_task_lists(self, user_id):
        """Get all task lists to which user was invited in.

        :param user_id: id of user.
        :return: list of user task lists.
        """
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
        """Get all subtasks that have parent_id equals to given task_id.

        :param task_id: id of task to get all subtasks.
        :return: list of subtasks.
        """
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
        """Get all tasks in task list with given id.

        :param task_list_id: id of task list.
        :return: list of tasks in task list.
        """
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
        """Get all tasks (except subtasks) in database.

        :return: list of all tasks.
        """
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
        """Get list of all users that at least once created or completed task.

        :return: list of ids.
        """
        users = set()
        with open(self.tasks_file, 'r+') as f:
            for line in f:
                task = jsonpickle.decode(line)
                if task.created_user:
                    users.add(task.created_user)
                if task.completed_user:
                    users.add(task.completed_user)

        with open(self.task_lists_file, 'r+') as f:
            for line in f:
                task_list = jsonpickle.decode(line)
                users.update(task_list.users)

        return users
