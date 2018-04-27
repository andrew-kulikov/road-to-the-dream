from src import TaskList


class Application:
    all_tasks = {}
    all_users = {}

    @staticmethod
    def get_task(task_id):
        return Application.all_tasks[task_id]

    @staticmethod
    def add_task(task):
        Application.all_tasks[task.id] = task

