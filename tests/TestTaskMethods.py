import unittest
from src import Task, TaskList, User, TaskStatus
import random
from datetime import datetime


class TestTaskMethods(unittest.TestCase):

    def test_create(self):
        task = Task()
        self.assertNotEquals(task.id, '')

    def test_sub_task_addition(self):
        parent = Task(description='sdfsdf')
        child = Task(description='erg', tags=['kek', 'lol', 'cheburek'], parent_id=parent.id)
        self.assertEquals(child.parent_id, parent.id)

    def test_deadline(self):
        task = Task(name='Good task', description='Simple task', end_date='20.05.2018 15:00')
        self.assertEquals(task.deadline, datetime.strptime('20.05.2018 15:00', '%d.%m.%Y %H:%M'))
        self.assertRaises(AttributeError, task.change, deadline='10.05.2018 15:00')


if __name__ == '__main__':
    unittest.main()
