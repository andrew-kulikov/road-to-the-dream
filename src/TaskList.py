import Task


class TaskList:
    def __init__(self, tasks):
        self.tasks = tasks

    def add_task(self, task):
        self.tasks[task.id] = task

    def group_by(self, rule):
        groupped_tasks = {}
        for id in self.tasks.keys:
            groupped_tasks[id] = self.tasks[id]
        return groupped_tasks
