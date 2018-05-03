from select import select


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
        used = {}

        def _print(tasks, level):
            tasks = [self.tasks[key] for key in tasks]
            for task in tasks:
                if task and not used.get(task.id, False):
                    used[task.id] = True
                    print('   ' * level, str(task))
                    _print(task.sub_tasks, level + 1)
        _print(self.tasks, 0)

    def get_task(self, task_id):
        return self.tasks.get(task_id, None)

    def complete_task(self, task_id):
        self.tasks[task_id].status = 'Completed'
        del self.tasks[task_id]

    def remove_task(self, task_id):
        tasks = list(self.tasks[task_id].sub_tasks)
        for task in tasks:
            self.remove_task(task)
        del self.tasks[task_id]

    def add_child(self, task_id, parent_id):
        self.tasks[task_id].parent_id = parent_id
        self.tasks[parent_id].add_sub_task(task_id)

    def __str__(self):
        s = []
        for task in self.tasks:
            s.append(str(self.tasks[task]))
        return '\n'.join(s)
