import unittest

class BaseRepository:
    def __init__(self):
        self.__storage = {}

    def get_unique_id(self):
        used_ids = sorted(self.__storage.keys())
        free_id = 1
        while free_id in used_ids:
            free_id += 1
        return free_id

    def add(self, new_entry):
        new_entry.id = self.get_unique_id()
        self.__storage[new_entry.id] = new_entry

    def delete(self, id):
        del self.__storage[id]

    def update(self, id, new_entry):
        self.delete(id)
        self.add(new_entry)

    def find(self, id):
        return self.__storage[id]

    def get_all(self):
        return list(self.__storage.values())


class MockObject:
    def __init__(self, id):
        self.__id = id

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        if self.id == None:
            self.id = id


class TestBaseRepository(unittest.TestCase):
    def setUp(self):
        self.repository = BaseRepository()
        for i in range(0, 10):
            self.repository.add(MockObject(i))

    def test_add(self):
        self.repository.add(MockObject(11))
        self.assertEqual(len(self.repository.get_all()), 11)
        self.assertEqual(self.repository.get_all()[-1].id, 11)

    def test_find(self):
        for i in range(0, 10):
            self.assertEqual(self.repository.find(i).id, i)
        self.assertRaises(KeyError, self.repository.find, 11)
        self.repository.add(MockObject(11))
        self.assertEqual(self.repository.get_all()[-1].id, 11)

    def test_delete(self):
        self.assertEqual(self.repository.find(2).id, 2)
        self.repository.delete(2)
        self.assertRaises(KeyError, self.repository.find, 2)

    def test_update(self):
        self.assertEqual(self.repository.find(2).id, 2)
        self.repository.update(2, MockObject(11))
        self.assertRaises(KeyError, self.repository.find, 2)
        self.assertEqual(self.repository.find(11).id, 11)

    def test_get_all(self):
        self.assertEqual(len(self.repository.get_all()), 10)