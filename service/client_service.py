from domain.client import Client
import unittest

from domain.client_formatter import ClientFormatter
from domain.client_validator import ClientValidator
from repository.client_repository import ClientRepository
from repository.rental_repository import RentalRepository


class ClientService:
    """
        Class that handles client events

        Attributes:
            repository(ClientRepository): where we store the clients data
            validator(ClientValidator): validates clients and their attributes
            formatter(ClientFormatter): formats the client and their attributes
            populate(bool): flag that indicates if you should populate the repository
    """
    def __init__(self, repository, validator, formatter, rental_repository, populate = False):
        self.__repository = repository
        self.__validator = validator
        self.__formatter = formatter
        self.__rental_repository = rental_repository
        if populate == True:
            self.__populate_repository()

    def __populate_repository(self):
        """
            Populates the repository
        """
        self.add(Client("1990122070000", "Devon", "Sanders"))
        self.add(Client("2990223070001", "Kyler", "Burke"))
        self.add(Client("2990317070002", "Mireya", "Macias"))
        self.add(Client("1990415070003", "Cesar", "Fields"))
        self.add(Client("2990501070004", "Hallie", "Yu"))
        self.add(Client("2990608070005", "Allison", "Duffy"))
        self.add(Client("2990705070006", "Kinley", "Richard"))
        self.add(Client("1990812070007", "Orion", "Solis"))
        self.add(Client("2990921070008", "Kale", "Deleon"))
        self.add(Client("1991011070009", "Conor", "Browning"))

    def add(self, new_client):
        """
            Adds a new client to the database

            Args:
                new_client(Client): new client to be added
        """
        self.__formatter.format(new_client)
        self.__validator.validate(new_client)

        self.__repository.add(new_client)

    def delete(self, CNP):
        """
            Deletes a client based on CNP

            Args:
                CNP(str): unique identifier for clients
        """
        CNP = self.__formatter.format_CNP(CNP)
        self.__validator.validate_CNP(CNP)

        self.__repository.delete(CNP)
        self.__rental_repository.delete_client(CNP)

    def update(self, CNP, new_client):
        """
            Updates a client based on CNP

            Args:
                CNP(str): unique identifier for clients
                new_client(Client): new attributes of the old client
        """
        CNP = self.__formatter.format_CNP(CNP)
        self.__validator.validate_CNP(CNP)
        self.__formatter.format(new_client)
        self.__validator.validate(new_client)

        self.__repository.update(CNP, new_client)
        self.__rental_repository.update_client(CNP, new_client)

    def find(self, CNP):
        """
            Finds a client based on CNP

            Args:
                CNP(str): unique identified for clients

            Returns:
                Client: client with CNP equal to the given one

            Raises:
                ValueError: if there isn't any client with the given CNP
        """
        CNP = self.__formatter.format_CNP(CNP)
        self.__validator.validate_CNP(CNP)

        return self.__repository.find(CNP)

    def get_list(self):
        """
            Gets list of clients

            Returns:
                list: list of clients from the database
        """
        return self.__repository.get_all()


class TestClientController(unittest.TestCase):
    def setUp(self):
        self.controller = ClientService(ClientRepository(), ClientValidator(), ClientFormatter(), RentalRepository())
        self.controller.add(Client("1990216079954", "Cazaciuc", "Valentin"))
        self.controller.add(Client("2990216079954", "Caza", "Vale"))
        self.controller.add(Client("1990216079999", "Gheorghe", "Ion"))

    def test_add(self):
        self.controller.add(Client("1990216070000", "Nume", "Prenume"))
        self.assertEqual(len(self.controller.get_list()), 4)
        self.assertEqual(self.controller.find("1990216070000").id, 4)

        self.assertRaises(ValueError, self.controller.add, Client("199021607005", "NumeDoi", "PrenumeDoi"))
        self.assertRaises(ValueError, self.controller.add, Client("199lf16070054", "NumeDoi", "PrenumeDoi"))
        self.assertRaises(ValueError, self.controller.add, Client("1990216070054", "Nume2", "PrenumeDoi"))
        self.assertRaises(ValueError, self.controller.add, Client("1990216070054", "NumeDoi", "Prenume2"))
        self.assertEqual(len(self.controller.get_list()), 4)
        self.assertRaises(ValueError, self.controller.find, "1990216070054")

        self.assertRaises(ValueError, self.controller.add, Client("1990216070000", "Nume2", "Prenume2"))
        self.assertEqual(len(self.controller.get_list()), 4)

    def test_get_list(self):
        self.assertEqual(len(self.controller.get_list()), 3)

    def test_delete(self):
        self.controller.delete("1990216079954")
        self.assertEqual(len(self.controller.get_list()), 2)
        self.assertRaises(ValueError, self.controller.find, "1990216079954")

        self.assertRaises(ValueError, self.controller.delete, "1990216079954")

    def test_update(self):
        self.controller.update("1990216079954", Client("1990216070000", "CazaciucDoi", "ValentinDoi"))
        self.assertEqual(len(self.controller.get_list()), 3)
        self.assertRaises(ValueError, self.controller.find, "1990216079954")
        self.assertEqual(self.controller.find("1990216070000").id, 1)

        self.assertRaises(ValueError, self.controller.update, "1990216079954", Client("1990216070000", "CazaciucDoi", "ValentinDoi"))

    def test_find(self):
        self.assertEqual(self.controller.find("1990216079954").id, 1)
        self.assertEqual(self.controller.find("2990216079954").id, 2)
        self.assertEqual(self.controller.find("1990216079999").id, 3)