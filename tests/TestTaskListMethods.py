import unittest
from src import TaskList, Task


class TestTaskListMethods(unittest.TestCase):

    def test_create(self):
        tasks = TaskList()
        self.assertIsInstance(tasks.tasks, dict)

    def test_add_task(self):
        tasks = TaskList()
        task = Task(description='ssfdf', tags=['lol', 'kek'])
        tasks.add_task(task)
        self.assertEquals(len(tasks.tasks), 1)
        self.assertIs(tasks.tasks[task.id], task)

    def test_task_change(self):
        tasks = TaskList()
        task = Task(description='ssfdf', tags=['lol', 'kek'])
        tasks.add_task(task)
        tasks.tasks[task.id].tags = ['beep']
        self.assertEquals(task.tags, ['beep'])


if __name__ == '__main__':
    unittest.main()
