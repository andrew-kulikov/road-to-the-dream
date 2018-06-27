import unittest
from rd_tracker import Task, TaskList, Controller, BasicConnector
import random
from datetime import datetime


class TestTaskMethods(unittest.TestCase):

    def setUp(self):
        self.connector = BasicConnector('lib_tests_tasks.json', 'lib_tests_task_lists.json')
        self.controller = Controller(self.connector)

    def test_create(self):
        task = Task()
        self.assertNotEquals(task.id, '')

    def test_sub_task_addition(self):
        parent = Task(description='sdfsdf')
        child = Task(description='erg', tags=['kek', 'lol', 'cheburek'], parent_id=parent.id)
        self.assertEquals(child.parent_id, parent.id)

    def test_deadline(self):
        task = Task(title='Good task', description='Simple task',
                    deadline=datetime.strptime('20.05.2018 15:00', '%d.%m.%Y %H:%M'))
        self.assertEquals(task.deadline, datetime.strptime('20.05.2018 15:00', '%d.%m.%Y %H:%M'))

    def test_create_list(self):
        task_list = TaskList()
        next_id = self.connector.get_next_task_list_id()
        list_id = self.controller.add_task_list(task_list)
        self.assertIsInstance(list_id, int)
        self.assertEquals(list_id, next_id)

    def test_add_task(self):
        task = Task(title='Task1', description='ssfdf', tags=['lol', 'kek'])
        free_id = self.connector.get_next_task_id()
        task_id = self.controller.add_task(task)
        self.assertIsInstance(task_id, int)
        self.assertEquals(task_id, free_id)
        task = self.controller.get_task(task_id)
        self.assertIsNotNone(task)
        self.assertIsInstance(task, Task)
        self.assertEquals(task.id, free_id)
        self.assertEquals(task.title, 'Task1')
    """
    def test_task_change(self):
        tasks = TaskList()
        task = Task(description='ssfdf', tags=['lol', 'kek'])
        tasks.add_task(task)
        tasks.tasks[task.id].tags = ['beep']
        self.assertEquals(task.tags, ['beep'])
    """


if __name__ == '__main__':
    unittest.main()
