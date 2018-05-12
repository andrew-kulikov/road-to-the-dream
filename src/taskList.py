from src import TaskStatus

class TaskList:
    def __init__(self, tasks=None):
        if tasks:
            if isinstance(tasks, dict):
                self.tasks = tasks
            elif isinstance(tasks, list):
                self.tasks = {}
                for task in tasks:
                    self.tasks[task.id] = task
        else:
            self.tasks = {}
        self.root_tasks = [task_id for task_id in self.tasks if self.tasks[task_id].parent_id == 0]

    def add_task(self, task):
        self.tasks[task.id] = task
        if task.id not in self.root_tasks and task.parent_id == 0:
            self.root_tasks.append(task.id)

    def sort_by(self, rule):
        self.root_tasks.sort(key=lambda x: rule(self.tasks[x]))
        for key in self.tasks:
            task = self.tasks[key]
            task.sub_tasks.sort(key=lambda x: rule(self.tasks[x]))

    def print_list(self):
        used = {}
        s = []

        def _print(tasks, level):
            tasks = [self.tasks[key] for key in tasks if key in self.tasks]
            for task in tasks:
                if task and not used.get(task.id, False):
                    used[task.id] = True
                    s.append('   ' * level + str(task))
                    _print(task.sub_tasks, level + 1)
        _print(self.root_tasks, 0)
        return s

    def get_task(self, task_id):
        return self.tasks.get(task_id, None)

    def get_failed(self):
        failed = []
        for task_id in self.tasks:
            if self.tasks[task_id].check_fail():
                failed.append(task_id)
        return failed

    def complete_task(self, task_id):
        if self.tasks[task_id].period:
            self.tasks[task_id].date += self.tasks[task_id].period
            return
        self.tasks[task_id].status = TaskStatus.COMPLETED
        del self.tasks[task_id]
        if task_id in self.root_tasks:
            self.root_tasks.remove(task_id)

    def remove_task(self, task_id):
        if task_id not in self.tasks:
            return
        tasks = list(self.tasks[task_id].sub_tasks)
        for task in tasks:
            self.remove_task(task)
        del self.tasks[task_id]
        if task_id in self.root_tasks:
            self.root_tasks.remove(task_id)

    def add_child(self, task_id, parent_id):
        msg = ''
        if task_id not in self.tasks:
            msg = 'task #' + task_id + ' does not exist'
            raise KeyError(msg)
        if parent_id and parent_id not in self.tasks:
            msg = 'task #' + parent_id + ' does not exist'
            raise KeyError(msg)

        if task_id in self.root_tasks:
            self.root_tasks.remove(task_id)
        self.tasks[task_id].parent_id = parent_id
        self.tasks[parent_id].add_sub_task(task_id)

    def __str__(self):
        s = []
        for task in self.tasks:
            s.append(str(self.tasks[task]))
        return '\n'.join(s)
