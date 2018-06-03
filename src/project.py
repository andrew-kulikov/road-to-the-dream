from src import TaskList
import hashlib


class Project:
    def __init__(self, name='Simple project'):
        self.id = 0
        self.name = name
        self.pending_tasks = TaskList({})
        self.completed_tasks = TaskList({})
        self.failed_tasks = TaskList({})
        self.users = set()
        self.id = hashlib.sha224(bytes(str(self), 'utf-8')).hexdigest()[:10]

    def add_user(self, user_login):
        self.users.add(user_login)

    def add_task(self, task, created_user_login):
        self.pending_tasks.add_task(task)
        if task.parent_id:
            self.pending_tasks.add_child(task.id, task.parent_id)
        if created_user_login not in self.users:
            self.add_user(created_user_login)
        task.created_user = created_user_login

    def edit_task(self, task_id, name=None, description=None, tags=None,
                  priority=None, deadline=None, period=None):
        if task_id not in self.pending_tasks.tasks:
            raise KeyError('Task with current id does not exist')
        self.pending_tasks.tasks[task_id].change(name=name, description=description, tags=tags, priority=priority,
                                                 deadline=deadline, period=period)

    def complete_task(self, task_id, completed_user):
        task_to_complete = self.pending_tasks.get_task(task_id)
        if not task_to_complete:
            return
        if task_to_complete.period:
            task_to_complete.deadline += task_to_complete.period
            return
        task_to_complete.completed_user = completed_user
        self.completed_tasks.add_task(task_to_complete)
        self.pending_tasks.complete_task(task_id)
        tasks = task_to_complete.sub_tasks
        if not tasks:
            return
        for task in tasks:
            self.complete_task(task, completed_user)

    def remove_task(self, task_id):
        if task_id in self.pending_tasks.tasks:
            self.pending_tasks.remove_task(task_id)
        elif task_id in self.completed_tasks.tasks:
            self.completed_tasks.remove_task(task_id)

    def update_tasks(self):
        failed_tasks = self.pending_tasks.get_failed()

        def _fail_task(task_id):
            task_to_fail = self.pending_tasks.get_task(task_id)
            task_to_fail.status = 'Failed'
            self.failed_tasks.add_task(task_to_fail)
            try:
                tasks = task_to_fail.sub_tasks
            except Exception:
                self.pending_tasks.remove_task(task_id)
                return
            if not tasks:
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

    def get_full_task_info(self, task_id):
        if task_id in self.pending_tasks.tasks:
            return self.pending_tasks.tasks[task_id].full_info()
        elif task_id in self.completed_tasks.tasks:
            return self.completed_tasks.tasks[task_id].full_info()
        elif task_id in self.failed_tasks.tasks:
            return self.failed_tasks.tasks[task_id].full_info()
        else:
            raise KeyError('Task with id #{id} does not exist'.format(id=task_id))

    def __str__(self):
        s = ''
        s += 'Id: {id}\nName: {name}\nPending tasks amount: {pending}\nCompleted tasks amount: {completed}\n'.format(
            id=self.id,
            name=self.name,
            pending=len(self.pending_tasks.tasks),
            completed=len(self.completed_tasks.tasks)
        )
        s += 'Users: ' + ', '.join(self.users)
        return s
