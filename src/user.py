from src import TaskList, TaskStatus
import random


class User:
    def __init__(self, login='vasya', password='123', name='vasya'):
        self.id = random.randint(0, 1000)
        self.login = login
        self._password = password
        self.name = name
        self.projects = set()
        self.pending_tasks = TaskList({})
        self.completed_tasks = TaskList({})
        self.failed_tasks = TaskList({})

    def change_password(self, old_password, new_password):
        if old_password == self._password:
            self._password = new_password
        else:
            raise Exception('Wrong password')

    def check_password(self, password):
        return self._password == password

    def add_task(self, task):
        self.pending_tasks.add_task(task)
        if task.parent_id:
            self.pending_tasks.add_child(task.id, task.parent_id)

    def edit_task(self, task_id, name=None, description=None, tags=None,
                  priority=None, deadline=None, period=None):
        if task_id not in self.pending_tasks.tasks:
            raise KeyError('Task with current id does not exist')
        self.pending_tasks.tasks[task_id].change(name=name, description=description, tags=tags, priority=priority,
                                                 deadline=deadline, period=period)

    def complete_task(self, task_id):
        task_to_complete = self.pending_tasks.get_task(task_id)
        if not task_to_complete:
            return
        if task_to_complete.period:
            task_to_complete.date += task_to_complete.period
            return
        self.completed_tasks.add_task(task_to_complete)
        self.pending_tasks.complete_task(task_id)
        tasks = task_to_complete.sub_tasks
        if not tasks:
            return
        for task in tasks:
            self.complete_task(task)

    def remove_task(self, task_id):
        if task_id in self.pending_tasks.tasks:
            self.pending_tasks.remove_task(task_id)
        elif task_id in self.completed_tasks.tasks:
            self.completed_tasks.remove_task(task_id)
        elif task_id in self.failed_tasks.tasks:
            self.failed_tasks.remove_task(task_id)

    def update_tasks(self):
        failed_tasks = self.pending_tasks.get_failed()

        def _fail_task(task_id):
            task_to_fail = self.pending_tasks.get_task(task_id)
            if not task_to_fail or task_to_fail.period:
                return
            task_to_fail.status = TaskStatus.FAILED
            self.failed_tasks.add_task(task_to_fail)
            tasks = task_to_fail.sub_tasks
            if not tasks:
                self.pending_tasks.remove_task(task_id)
                return
            for task in tasks:
                _fail_task(task)
            self.pending_tasks.remove_task(task_id)
        for task in failed_tasks:
            _fail_task(task)

    def move_task(self, source_id, destination_id):
        if source_id not in self.pending_tasks.tasks or destination_id not in self.pending_tasks.tasks:
            raise KeyError('No task with current id')
        cur_id = destination_id
        while cur_id:
            cur_id = self.pending_tasks.tasks[cur_id].parent_id
            if cur_id == source_id:
                raise RecursionError('Destination task is one of the source task sub tasks')
        try:
            self.pending_tasks.add_child(source_id, destination_id)
        except Exception as e:
            raise e

    def __str__(self):
        return self.login + ' (' + self.name + ')'
