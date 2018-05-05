from datetime import datetime
import hashlib


class Task:
    def __init__(self, parent_id=0, name='Simple task', description='', tags=None):
        self.date = datetime.now()
        self.sub_tasks = []
        self.name = name
        self.description = description
        self.tags = tags
        self.parent_id = parent_id
        self.status = 'In progress'
        self.id = 0
        self.id = hashlib.sha224(bytes(str(self), 'utf-8')).hexdigest()[:10]

    def __str__(self):
        s = ''
        s += 'Task #{id} | {name} | {status} | {date}'.format(
            id=self.id,
            name=self.name,
            status=self.status,
            date=self.date,
            descr=self.description
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
