import random
from src import TaskList


class Project:
    def __init__(self, name='Simple project'):
        self.id = random.randint(0, 1000)
        self.name = name
        self.pending_tasks = TaskList({})
        self.completed_tasks = TaskList({})
        self.users = set()

    def add_user(self, user_login):
        self.users.add(user_login)

    def add_task(self, task, created_user_login):
        if created_user_login not in self.users:
            self.add_user(created_user_login)
        task.created_user = created_user_login
        self.pending_tasks.add_task(task)
        if task.parent_id:
            self.pending_tasks.add_child(task.id, task.parent_id)

    def complete_task(self, task_id, completed_user):
        task_to_complete = self.pending_tasks.get_task(task_id)
        task_to_complete.completed_user = completed_user
        self.completed_tasks.add_task(task_to_complete)
        self.pending_tasks.complete_task(task_id)
        try:
            tasks = task_to_complete.sub_tasks
        except KeyError as e:
            raise e
        except AttributeError as e:
            raise e
        if not tasks:
            return
        for task in tasks:
            self.complete_task(task, completed_user)

    def remove_task(self, task_id):
        if task_id in self.pending_tasks.tasks:
            self.pending_tasks.remove_task(task_id)
        elif task_id in self.completed_tasks.tasks:
            self.completed_tasks.remove_task(task_id)

    def move_task(self, source_id, destination_id):
        if source_id not in self.pending_tasks.tasks or destination_id not in self.pending_tasks.tasks:
            raise KeyError('No task with current id')
        cur_id = destination_id
        while cur_id:
            cur_id = self.pending_tasks.tasks[cur_id].parent_id
            if cur_id == source_id:
                raise RecursionError('Destination task is one of the source task sub tasks')
        self.pending_tasks.add_child(source_id, destination_id)

    def __str__(self):
        s = ''
        s += 'Name: {name}\nPending tasks amount: {pending}\nCompleted tasks amount: {completed}\n'.format(
            name=self.name,
            pending=len(self.pending_tasks.tasks),
            completed=len(self.completed_tasks.tasks)
        )
        s += 'Users: ' + ', '.join(self.users)
        return s
