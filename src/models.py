"""
models module is designed to store basic object models of the program

Public classes:

'Task': basic library class to work with. Contains information about the task:
title, id, description, deadline, ... (for more information see Task documentation).
'TaskList': representation of task list. Contains information about task list:
 name, id, users. For more information see TaskList documentation.
"""

from datetime import datetime


class Task:
    """Task class

    Designed to store task object information.

     Attributes:
        parent_id (int, default None): Id of parent task.
        title (str, default None): Task name, should be informative and short.
        description (str, default None): Additional information for the task.
        tags (:obj:`list`, default None): Task tags (should be list of strings).
        priority(int, default 0): Task priority - integer number in range (0, 10),
                                         0 - highest priority, 9 - lowest.
        deadline(datetime, default None): Date of deadline in format [DD.MM.YYYY hh:mm].
                                        If None, task has no time limit.
        period_val(str, default None): Period of repeating in format [d | w | m | y], where
                                    d - day, w - week, m - month, y - year. If None, task is not repeating.
        period_count(int, default None): Amount of times to skip period. For example if got period_count = 2
                                        and period_val = d, task will repeat every 2 days.
        repeat_days(:obj:`list`, default None): Days of week to repeat task if task repeat period is week.
                                        Should be in format [{1-7}] where 1 - Monday, 7 - Sunday.
        created (datetime): Date and time of task creation.
        status (str): Task status. Should be one of given values: 'pending', 'completed'
        task_list (int, default None): Id of task list that contains task.
        created_user (int, default None): Id of created user.
        completed_user (int, default None): Id of completed user.

    """

    def __init__(self, title=None, description=None, created=None, deadline=None, created_user=None,
                 completed_user=None, tags=None, task_list=None, priority=None, status=None,
                 repeat_days=None, period_count=None, period_val=None, parent_id=None):
        self.__id = None
        self.title = title
        self.description = description
        if not created:
            self.created = datetime.now()
        else:
            self.created = created
        self.deadline = deadline
        self.created_user = created_user
        self.completed_user = completed_user
        self.tags = tags
        if not tags:
            self.tags = []
        self.task_list = task_list
        self.priority = priority
        self.status = status
        if not status:
            self.status = 'pending'
        self.repeat_days = repeat_days
        self.period_count = period_count
        self.period_val = period_val
        self.parent_id = parent_id

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, val):
        if not isinstance(val, int):
            raise ValueError
        self.__id = val

    def __str__(self):
        return '#' + str(self.id) + ' ' + self.title


class TaskList:
    def __init__(self, name=None, is_private=True, users=None, created_user=None):
        self.__id = None
        self.name = name
        self.is_private = is_private
        self.users = users
        self.created_user = created_user

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, val):
        if not isinstance(val, int):
            raise ValueError
        self.__id = val

    def __str__(self):
        return self.name
