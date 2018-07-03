"""controllers module
Designed to give basic interface to interact with Task and TaskList.
Contains Controller class that implements those basic methods.

All methods have similar structure:
1. Gets object from database.
2. Applies some changes or filter data according given rules.
3. Raises exceptions if given data or queries is not valid.
4. Saves changed data in database and returns it.

Database communication interface is represented by __connector.

Module uses:
    dateutil.relativedelta: helps with issues with periodic tasks completion.

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
from dateutil.relativedelta import relativedelta, MO, TH, TU, SA, SU, FR, WE


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
        """Remove task list from database with all tasks.

        :param task_list_id: id of list to delete.
        :return: None
        :raises
        'KeyError': if task list with given id does not exist.
        """
        task_list = self.__connector.get_task_list(task_list_id)
        tasks = self.get_task_list_tasks(task_list.id)
        for task in tasks:
            self.delete_task(task.id)

    def get_subtasks(self, task_id):
        """Get all subtasks that have parent_id equals to given task_id.

        :param task_id: id of task to get all subtasks.
        :return: list of subtasks.
        :raises
        'KeyError': if task with given id does not exist.
        """
        tasks = self.__connector.get_subtasks(task_id)
        self.__connector.save_tasks(tasks, 'a+')
        return tasks

    def get_all_tasks(self):
        """Get all tasks (except subtasks) in database.

        :return: list of all tasks.
        """
        tasks = self.__connector.get_all_tasks()
        self.__connector.save_tasks(tasks, 'a+')
        return tasks

    def get_task(self, task_id):
        """Get task with given id from database.

        :param task_id: id of task to pick from db.
        :return: task with given id.
        :raises
        'KeyError': if task was not found in database.
        """
        task = self.__connector.get_task(task_id)
        self.__connector.save_task(task)
        return task

    def complete_task(self, task_id):
        """Complete tasks with all subtasks.

        If task has no period, function will recursively complete all subtasks of given task (their
        status will be changed to completed).
        Otherwise, task deadline will shift to the deadline + period_val * period_count. All subtasks
        in task subtree will be marked as pending.

        :param task_id: id of task to complete.
        :return: None
        :raises
        'KeyError': if task id was not found in the database.
        """
        task = self.__connector.get_task(task_id)
        self.__connector.save_task(task)

        def set_subtasks_status(task_id, status='completed'):
            # utility function that designed to walk task subtasks tree and change their status.
            subtasks = self.__connector.get_subtasks(task_id)
            if not subtasks or not len(subtasks):
                return
            for subtask in subtasks:
                subtask.status = 'C'
                self.__connector.save_task(subtask)
                set_subtasks_status(subtask.id, status)

        if task.period_val:
            # if task hasperiod, we change deadline and mark all subtasks as pending
            set_subtasks_status(task.id, 'pending')
            if task.period_val == 'D':
                task.deadline += relativedelta(days=+task.period_count)
            elif task.period_val == 'W':
                # check for days of week if period is week
                if task.repeat_days and len(task.repeat_days):
                    last_weekday = task.deadline.weekday()
                    days = [MO, TU, WE, TH, FR, SA, SU]
                    new_week = True
                    for day in task.repeat_days:
                        if day - 1 > last_weekday:
                            new_week = False
                            task.deadline += relativedelta(weekday=days[day - 1])
                            break
                    if new_week:
                        first_day_number = task.repeat_days[0] - 1
                        task.deadline += relativedelta(weeks=task.period_count - 1, weekday=days[first_day_number])
                else:
                    task.deadline += relativedelta(weeks=+task.period_count)
            elif task.period_val == 'M':
                task.deadline += relativedelta(months=+task.period_count)
            elif task.period_val == 'Y':
                task.deadline += relativedelta(years=+task.period_count)
        else:
            # if task has no period, just mark all subtasks as completed
            set_subtasks_status(task.id)

    def edit_task(self, task_id, attrs):
        """Replace attributes of task with given id by new attributes.

        :param task_id: id of task to edit.
        :param attrs: dict of new attributes in format "attribute name: value". Example: {'title': 'task1'}.
        :return: None
        :raises
        'KeyError': if task with given id does not exist.
        """
        task = self.__connector.get_task(task_id)
        if 'title' in attrs:
            task.title = attrs['title']
        self.__connector.save_task(task)

    def edit_task_list(self, task_list_id, attrs):
        """Replace attributes of task list with given id by new attributes.

        If new value of `is_private` attribute is True, all users will be removed from task list.

        :param task_list_id: id of task list to edit.
        :param attrs: dict of new attributes in format "attribute name: value". Example: {'name': 'list1'}.
        :return: None
        :raises
        'KeyError': if task list with given id does not exist.
        """
        task_list = self.__connector.get_task_list(task_list_id)
        if 'name' in attrs:
            if not isinstance(attrs['name'], str):
                self.__connector.save_task_list(task_list)
                raise AttributeError('Given task list name is not not string')
            task_list.name = attrs['name']

        if 'is_private' in attrs:
            if not isinstance(attrs['is_private'], bool):
                self.__connector.save_task_list(task_list)
                raise AttributeError('Given task list privacy is not not bool')
            task_list.is_private = attrs['is_private']
            if task_list.is_private:
                tasks = self.__connector.get_task_list_tasks(task_list_id)
                for task in tasks:
                    task.task_list = None
                self.__connector.save_tasks(tasks, mode='a')
                task_list.users.clear()
                task_list.users.add(task_list.created_user)

        self.__connector.save_task_list(task_list)

    def invite_user(self, task_list_id, user_id):
        """Add user with given id to the task list.

        :param task_list_id: Id of task list you want to add user in.
        :param user_id: Id of user you want to add in task list.
        :return:
        :raises
        'KeyError': if task list with given id does not exist.
        """
        task_list = self.__connector.get_task_list(task_list_id)
        task_list.users.append(user_id)
        self.__connector.save_task_list(task_list)

    def get_user_task_lists(self, user_id):
        """Get all task lists to which user was invited in.

        :param user_id: id of user.
        :return: list of user task lists.
        """
        lists = self.__connector.get_user_task_lists(user_id)
        self.__connector.save_task_lists(lists, 'a+')
        return lists

    def get_task_list_tasks(self, task_list_id):
        """Get all tasks in task list with given id.

        :param task_list_id: id of task list.
        :return: list of tasks in task list.
        :raises
        'KeyError': if task list with given id does not exist.
        """
        tasks = self.__connector.get_task_list_tasks(task_list_id)
        self.__connector.save_tasks(tasks, 'a+')
        return tasks

    def change_connector(self, connector):
        """Replace db connector with new connector, new connector should
        implement BaseConnector interface.

        :param connector: new db connector.
        :return:
        """
        self.__connector = connector

    def sort_tasks(self, sort_type):
        """Sort tasks in given order.

        Sort all tasks and then their subtasks in given order.

        :param sort_type: Task field by which they will be sorted. Possible choices: 'title', 'deadline', 'priority'
        :return: list of sorted tasks that have parent_id equals to None.
        :raises
        'AttributeError': if sort type not in possible choices.
        """
        sorts = {
            'title': lambda task: task.title,
            'deadline': lambda task: task.deadline,
            'priority': lambda task: task.priority}
        if sort_type not in sorts:
            # self.logger.error('Cannot sort with parameter ' + str(sort_type))
            raise AttributeError('No such sort type')
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
