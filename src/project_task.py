from src import Task


class ProjectTask(Task):
    def __init__(self, parent_id=0, name='Simple task', description='', tags=None, created_user=None):
        self.created_user = created_user
        self.completed_user = None
        super().__init__(parent_id, name, description, tags)

    def __str__(self):
        s = super().__str__()
        completed_user = self.completed_user
        if not completed_user:
            completed_user = '_'
        s += ' | ' + self.created_user + '\\' + str(completed_user)
        return s
