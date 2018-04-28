class TaskList:
    def __init__(self, tasks=None, name='Simple_list'):
        self.name = name
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

    def get_task(self, task_id):
        return self.tasks.get(task_id, None)

    def remove_task(self, task_id):
        if task_id in self.tasks:
            self.tasks[task_id].status = 'Completed'
            self.tasks[task_id].parent = None
            self.tasks[task_id].parent.remove_sub_task(task_id)

    def add_child(self, task_id, parent_id):
        self.tasks[task_id].parent_id = parent_id
        self.tasks[parent_id].add_sub_task(task_id)
