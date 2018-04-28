import unittest
from src import Task, TaskList, User


class TestTaskMethods(unittest.TestCase):

    def test_create(self):
        task = Task()
        self.assertNotEquals(task.id, '')

    def test_numeration(self):
        size = 10000
        ids = set()
        for i in range(size):
            task = Task()
            ids.add(task.id)
        self.assertEquals(len(ids), size)

    def test_sub_task_addition(self):
        parent = Task(description='sdfsdf')
        child = Task(description='erg', tags=['kek', 'lol', 'cheburek'], parent_id=parent.id)
        self.assertEquals(child.parent_id, parent.id)


if __name__ == '__main__':
    unittest.main()
