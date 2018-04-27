from src import Task


class TaskList:
    def __init__(self, tasks=None):
        if tasks:
            self.tasks = tasks
        else:
            self.tasks = {}

    def add_task(self, task):
        self.tasks[task.id] = task

    def group_by(self, rule):
        good_tasks = {}
        for key in self.tasks:
            task = self.tasks[key]
            if rule(task):
                good_tasks[key] = task
        return good_tasks

    def print_list(self):
        def _print(tasks, level):
            for task in tasks:
                print('\t' * level, str(task))
                _print(task.sub_tasks, level + 1)
        _print([self.tasks[key] for key in self.tasks], 0)
