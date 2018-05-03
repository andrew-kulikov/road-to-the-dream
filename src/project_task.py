from src import Task


class ProjectTask(Task):
    def __init__(self, parent_id=0, name='Simple task', description='', tags=None):
        super().__init__(parent_id, name, description, tags)
        self.created_user = None
        self.completed_user = None
