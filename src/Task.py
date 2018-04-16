from datetime import datetime


class Task:
    def __init__(self):
        self.date = datetime.now()
        self.sub_tasks = []
        self.description = 'Simple task'
        self.tags = []
        self.status = 'In process'
        self.id = id(self)

    def __str__(self):
        s = ''
        s += 'Task #{id}\nStatus: {status}\nDate: {date}\nDescription: {descr}'.format(
            id=self.id,
            status=self.status,
            date=self.date,
            descr=self.description
        )
        return s
