import unittest
from src import Task, TaskList, User
import random


class TestTaskMethods(unittest.TestCase):

    def test_create(self):
        task = Task()
        self.assertNotEquals(task.id, '')

    def test_sub_task_addition(self):
        parent = Task(description='sdfsdf')
        child = Task(description='erg', tags=['kek', 'lol', 'cheburek'], parent_id=parent.id)
        self.assertEquals(child.parent_id, parent.id)


if __name__ == '__main__':
    unittest.main()
