from datetime import datetime


class Task:
    def __init__(self):
        self.date = datetime.now()
        self.sub_tasks = []
        self.description = 'Simple task'
        self.tags = []
        self.status = 'In process'

