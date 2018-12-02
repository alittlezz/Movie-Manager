import unittest

from domain.client import Client


class ClientRepository:
    """
        Class that stores clients

        Attributes:
            clients(dictionary): list of clients stored
    """
    def __init__(self):
        self.__clients = {}

    def get_unique_id(self):
        """
            Returns the first free id in range [1, ...]

            Returns:
                int: first free index
        """
        used_ids = sorted([client.id for client in self.__clients.values()])
        free_id = 1
        while free_id in used_ids:
            free_id += 1
        return free_id

    def add(self, new_client):
        """
            Adds a new client to repository

            Args:
                new_client(Client): client to be added to repository

            Raises:
                ValueError: if client with new_client CNP already exists in repostiroy
        """
        try:
            self.find(new_client.CNP)
            is_duplicate = True
        except ValueError:
            new_client.id = self.get_unique_id()
            self.__clients[new_client.CNP] = new_client
            is_duplicate = False

        if is_duplicate == True:
            raise ValueError("Exista deja client cu acest CNP")

    def delete(self, CNP):
        """
            Removes a client from repository

            Args:
                CNP(str): CNP of the client to be removed
        """
        self.find(CNP)
        del self.__clients[CNP]

    def update(self, CNP, new_client):
        """
            Updates a client from repository:

            Args:
                CNP(str): CNP of the client to be updated
                new_client(Client): new value for client
        """
        self.delete(CNP)
        self.add(new_client)

    def find(self, CNP):
        """
            Finds a client from repository

            Args:
                CNP(str): CNP of the client to be searched

            Raises:
                ValueError: if client with CNP doesn't exist in repository
        """
        try:
            return self.__clients[CNP]
        except KeyError:
            raise ValueError("Nu exista client cu acest CNP")

    def get_all(self):
        """
            Returns list of clients from repository

            Returns:
                list: list of clients from repository
        """
        return list(self.__clients.values())


class TestClientRepository(unittest.TestCase):
    def setUp(self):
        self.repository = ClientRepository()

    def test_get_all(self):
        self.assertEqual(len(self.repository.get_all()), 0)
        self.repository.add(Client("1990216070054"))
        self.assertEqual(len(self.repository.get_all()), 1)
        self.repository.add(Client("1990216070000"))
        self.assertEqual(len(self.repository.get_all()), 2)

    def test_add(self):
        self.repository.add(Client("1990216070099"))
        self.assertEqual(len(self.repository.get_all()), 1)
        self.repository.add(Client("1990216070033"))
        self.assertEqual(len(self.repository.get_all()), 2)
        self.repository.add(Client("1990216070022"))
        self.assertEqual(len(self.repository.get_all()), 3)
        self.assertRaises(ValueError, self.repository.add, Client("1990216070099"))
        self.assertEqual(len(self.repository.get_all()), 3)

    def test_delete(self):
        self.repository.add(Client("1990216070099"))
        self.repository.add(Client("1990216070022"))
        self.repository.delete("1990216070099")
        self.assertEqual(len(self.repository.get_all()), 1)
        self.assertRaises(ValueError, self.repository.delete, "1990216070000")
        self.assertEqual(len(self.repository.get_all()), 1)

    def test_find(self):
        self.repository.add(Client("1990216070099"))
        self.repository.find("1990216070099")
        self.repository.add(Client("1990216070000"))
        self.repository.find("1990216070000")
        self.assertRaises(ValueError, self.repository.find, "1990216070054")

    def test_update(self):
        self.repository.add(Client("1990216070099"))
        self.repository.update("1990216070099", Client("1990216070000"))
        self.assertEqual(len(self.repository.get_all()), 1)
        self.repository.find("1990216070000")
        self.assertRaises(ValueError, self.repository.find, "1990216070099")

    def test_get_unique_id(self):
        self.assertEqual(self.repository.get_unique_id(), 1)
        self.repository.add(Client("1990216070099"))
        self.assertEqual(self.repository.get_unique_id(), 2)
        self.repository.add(Client("1990216070054"))
        self.assertEqual(self.repository.get_unique_id(), 3)
        self.repository.delete("1990216070099")
        self.assertEqual(self.repository.get_unique_id(), 1)