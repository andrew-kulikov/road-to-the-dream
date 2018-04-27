from datetime import datetime


class Task:
    ID = 0

    def __init__(self, parent=None):
        self.date = datetime.now()
        self.sub_tasks = []
        self.description = 'Simple task'
        self.tags = []
        self.parent = parent
        self.status = 'In process'
        Task.ID += 1
        self.id = Task.ID

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
        sub_task.parent = self.id
        self.sub_tasks.append(sub_task.id)
