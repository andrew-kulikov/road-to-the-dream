from datetime import datetime, timedelta
import hashlib


class Task:
    def __init__(self, parent_id=0, name='Simple task', description='',
                 tags=None, priority=0, end_date=None, period=None):
        self.date = None
        if end_date:
            self.parse_date(end_date)
        self.period = period
        if period:
            self.parse_period(period)
        self.sub_tasks = []
        self.name = name
        self.description = description
        self.tags = tags
        self.parent_id = parent_id
        self.status = 'In progress'
        self.id = 0
        self.priority = 0
        if 0 <= priority <= 9:
            self.priority = priority
        self.id = hashlib.sha224(bytes(str(self), 'utf-8')).hexdigest()[:10]

    def parse_date(self, date):
        self.date = datetime.strptime(date, '%d.%m.%Y %H:%M')

    def parse_period(self, period):
        if period == 'd':
            self.period = timedelta(days=1)
        if period == 'w':
            self.period = timedelta(weeks=1)
        if period == 'm':
            self.period = timedelta(days=30)
        if period == 'y':
            self.period = timedelta(days=365)
        else:
            raise AttributeError('Unknown time period')

    def __str__(self):
        s = ''
        s += 'Task #{id} | {name} | {status} | {date} | Pr: {priority}'.format(
            id=self.id,
            name=self.name,
            status=self.status,
            date=self.date,
            descr=self.description,
            priority=self.priority
        )
        return s

    def change(self, date=None, description=None, tags=None, status=None):
        if date:
            self.date = date
        if description:
            self.description = description
        if tags:
            self.tags = tags
        if status:
            self.status = status

    def add_sub_task(self, sub_task_id):
        if sub_task_id not in self.sub_tasks:
            self.sub_tasks.append(sub_task_id)

    def remove_sub_task(self, sub_task_id):
        self.sub_tasks.remove(sub_task_id)
