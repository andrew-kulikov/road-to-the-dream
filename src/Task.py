from datetime import datetime
import hashlib


class Task:
    ID = 0

    def __init__(self, parent_id=0, description='Simple task', tags=None, status='In progress'):
        self.date = datetime.now()
        self.sub_tasks = set()
        self.description = description
        self.tags = tags
        self.parent_id = parent_id
        self.status = status
        Task.ID += 1
        self.id = Task.ID
        self.id = hashlib.sha224(bytes(str(self), 'utf-8')).hexdigest()

    def __str__(self):
        s = ''
        s += 'Task #{id}\nStatus: {status}\nDate: {date}\nDescription: {descr}'.format(
            id=self.id,
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

    def add_sub_task(self, sub_task):
        sub_task.parent_id = self.id
        self.sub_tasks.add(sub_task.id)

    def remove_sub_task(self, sub_task_id):
        self.sub_tasks.remove(sub_task_id)
