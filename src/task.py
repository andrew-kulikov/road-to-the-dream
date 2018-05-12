"""Task module. 
Contains :class:`Task`.
Uses datetime and hashlib modules.
"""
from datetime import datetime
from src.tools import parsers
from enum import Enum
import hashlib


class TaskStatus(Enum):
    COMPLETED = 'completed'
    PENDING = 'in progress'
    FAILED = 'failed'


class Task:
    """Task class
    
     Args:
        parent_id (str, default 0): Id of parent task.
        name (str, default 'Simple task'): Task name, should be informative and short.
        description (str, default ''): Additional information for the task.
        tags (:obj:`list`, default None): Task tags.
        priority(:obj:`int`, default 0): Task priority - integer number in range (0, 10),
                                         0 - highest priority, 9 - lowest.
        end_date(str, default None): Date of deadline in format [DD.MM.YYYY hh:mm]. 
                                    If None, task has no time limit. 
        period(str, default None): Period of repeating in format [d | w | m | y], where
                                    d - day, w - week, m - month, y - year. If None, task is not repeating.
     
     Attributes:
        parent_id (str, default 0): Id of parent task.
        name (str, default 'Simple task'): Task name, should be informative and short.
        description (str, default ''): Additional information for the task.
        tags (:obj:`list`, default None): Task tags.
        priority(:obj:`int`, default 0): Task priority - integer number in range (0, 10),
                                         0 - highest priority, 9 - lowest.
        end_date(str, default None): Date of deadline in format [DD.MM.YYYY hh:mm]. 
                                    If None, task has no time limit. 
        period(str, default None): Period of repeating in format [d | w | m | y], where
                                    d - day, w - week, m - month, y - year. If None, task is not repeating.
    
    """
    def __init__(self, parent_id=0, name='Simple task', description='',
                 tags=None, priority=0, end_date=None, period=None):
        self.date = None
        if end_date:
            self.parse_date = parsers.parse_date(end_date)
        self.period = period
        if period:
            if not end_date:
                raise Exception('Simple task cannot be repeating')
            self.parse_period = parsers.parse_period(period)
        self.sub_tasks = []
        self.name = name
        self.description = description
        self.tags = tags
        self.parent_id = parent_id
        self.status = TaskStatus.PENDING
        self.id = 0
        self.priority = 0
        if 0 <= priority <= 9:
            self.priority = priority
        self.id = hashlib.sha224(bytes(str(self), 'utf-8')).hexdigest()[:10]

    def check_fail(self):
        """Check task state
        
        Returns:
            bool: True if task is overdue, False otherwise.
        
        """
        if not self.date:
            return False
        if self.date < datetime.now():
            if self.period:
                while self.date < datetime.now():
                    self.date += self.period
                return False
            self.status = TaskStatus.FAILED
            return True
        if self.period:
            return False
        return False

    def change(self, description=None, tags=None,
               name=None, priority=None, deadline=None, period=None):
        if description:
            self.description = description
        if tags:
            self.tags = tags
        if name:
            self.name = name
        if priority and 0 <= priority <= 9:
            self.priority = priority
        if deadline:
            self.parse_date(deadline)
        if period:
            self.parse_period(period)

    def add_sub_task(self, sub_task_id):
        if sub_task_id not in self.sub_tasks:
            self.sub_tasks.append(sub_task_id)

    def remove_sub_task(self, sub_task_id):
        self.sub_tasks.remove(sub_task_id)

    def full_info(self):
        s = ''
        s += 'Task #{id}\nName: {name}\nStatus: {status}\nDeadline: {date}\nPriority: {priority}\nDescription: {description}\nParent id: {parent_id}\nTags: {tags}'.format(
            id=self.id,
            name=self.name,
            status=self.status.value,
            date=self.date,
            descr=self.description,
            priority=self.priority,
            description=self.description,
            parent_id=self.parent_id,
            tags=', '.join(self.tags)
        )
        return s

    def __str__(self):
        s = 'Task #{id} | {name} | {status} | Deadline: {date} | Priority: {priority}'.format(
            id=self.id,
            name=self.name,
            status=self.status.value,
            date=self.date,
            descr=self.description,
            priority=self.priority
        )
        return s
