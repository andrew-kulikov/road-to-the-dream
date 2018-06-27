from datetime import datetime


class Task:

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
