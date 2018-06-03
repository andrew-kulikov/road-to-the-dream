"""taskList module. 
Contains :class:`TaskList`.
"""
from src import TaskStatus


class TaskList:
    """Task class

         Args:
            tasks (:obj:`dict` or :obj:`list`, default None): Tasks dict or array to initialize class field.

         Attributes:
            tasks (:obj:`dict`): Tasks that contains given instance of taskList.
            root_tasks (:obj:`dict`): Tasks that has no parent task. 
            
        """
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
        """Add task to task list
        
        Args:
            task (:obj:`Task`): Task to be added to the task list.
        
        Returns:
            None
        """
        self.tasks[task.id] = task
        if task.id not in self.root_tasks and task.parent_id == 0:
            self.root_tasks.append(task.id)

    def sort_by(self, rule):
        """Sort tasks by given rule
        
        Args:
            rule (func): function that takes :obj:`Task` as argument and returns some parameter of task to sort by.
        
        Returns:
            None
        """
        # at first sort all root tasks.
        self.root_tasks.sort(key=lambda x: rule(self.tasks[x]))
        # then sort subtasks of all tasks according given rule.
        for key in self.tasks:
            task = self.tasks[key]
            task.sub_tasks.sort(key=lambda x: rule(self.tasks[x]))

    def print_list(self):
        """Give string representation of taskList
        
        Forms task tree according to their levels.
        
        Example:
            Task #013b7784fd | Task1 | in progress | Deadline: None | Priority: 0
                Task #ecf553b571 | Task2 | in progress | Deadline: None | Priority: 0
         
        Returns:
            str: task list string representation.
        """
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
        """Get instance of task with given id
        
        Args:
            task_id (str): id of task to get.
        
        Returns:
            :obj:`Task`: if task with given id exists in task list.
            None: otherwise.
        """
        return self.tasks.get(task_id, None)

    def get_failed(self):
        """Get list of failed tasks.
        
        Checks all tasks state and returns list of overdue tasks.
        
        Returns:
             :obj:`list`: list of failed tasks.
        """
        failed = []
        for task_id in self.tasks:
            if self.tasks[task_id].check_fail():
                failed.append(task_id)
        return failed

    def complete_task(self, task_id):
        """Complete tasks with given id.
        
        If task is periodic, it's deadline just moves to deadline + period, else task status becomes 'Completed' and 
          task deleted from task list.
        
        Args:
            task_id (str): Id of task to complete.
        
        Returns:
            None.
        """
        if self.tasks[task_id].period:
            self.tasks[task_id].deadline += self.tasks[task_id].period
            return
        self.tasks[task_id].status = TaskStatus.COMPLETED
        del self.tasks[task_id]
        if task_id in self.root_tasks:
            self.root_tasks.remove(task_id)

    def remove_task(self, task_id):
        """Remove task from task list.
        
        Recursively removes task with all subtasks.
         
        Args:
            task_id (str): Id of task 
        """
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
