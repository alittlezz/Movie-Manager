import unittest


class Client:
    """
        Class for the client entity

        Attributes:
            id(int): unique id for the client
            CNP(str): unique id for the client, made of 13 digits
            surname(str): surname of the client
            name(str): name of the client
    """
    def __init__(self, CNP, surname = None, name = None, id = None):
        self.__id = id
        self.__CNP = CNP
        self.__surname = surname
        self.__name = name

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        if self.__id == None:
            self.__id = id
        else:
            raise Exception("Id already set")

    @property
    def CNP(self):
        return self.__CNP

    @CNP.setter
    def CNP(self, CNP):
        self.__CNP = CNP

    @property
    def surname(self):
        return self.__surname

    @surname.setter
    def surname(self, surname):
        self.__surname = surname

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def full_name(self):
        return self.__surname + ' ' + self.__name

    @full_name.setter
    def full_name(self, full_name):
        self.__surname, self.__name = full_name.split()

    def copy(self):
        return Client(self.CNP, self.surname, self.name)

    def __repr__(self):
        representation = ""
        representation += "CNP: " + self.CNP + '\n'
        representation += "Nume intreg: " + self.full_name + '\n'
        return representation

    def __eq__(self, other):
        return self.CNP == other.CNP

    def __hash__(self):
        return hash(self.CNP)

class ClientDTO(Client):
    def __init__(self, client, no_rentals = 0):
        super().__init__(client.CNP, client.surname, client.name, id = client.id)
        self.__no_rentals = no_rentals

    @property
    def no_rentals(self):
        return self.__no_rentals

    @no_rentals.setter
    def no_rentals(self, no_rentals):
        self.__no_rentals = no_rentals

def get_clientDTO_data_from_list(clients):
    data = []
    data.append(["ID", "CNP", "Nume", "Prenume", "Inchirieri"])
    for client in clients:
        attributes = list(map(str, [client.id, client.CNP, client.surname, client.name, client.no_rentals]))
        data.append(attributes)
    return data

def get_client_data_from_list(clients):
    data = []
    data.append(["ID", "CNP", "Nume", "Prenume"])
    for client in clients:
        attributes = list(map(str, [client.id, client.CNP, client.surname, client.name]))
        data.append(attributes)
    return data

class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = Client("1990216079954", "Cazaciuc", "Valentin")

    def test_setters(self):
        self.assertEqual(self.client.CNP, "1990216079954")
        self.assertEqual(self.client.surname, "Cazaciuc")
        self.assertEqual(self.client.name, "Valentin")
        self.assertEqual(self.client.full_name, "Cazaciuc Valentin")

    def test_getter(self):
        self.client.CNP = "2990216079954"
        self.assertEqual(self.client.CNP, "2990216079954")

        self.client.surname = "Caza"
        self.assertEqual(self.client.surname, "Caza")

        self.client.name = "Vale"
        self.assertEqual(self.client.name, "Vale")

        self.assertEqual(self.client.full_name, "Caza Vale")

    def test_eq(self):
        other = Client("1990216079954", "Caza", "Vale")
        self.assertEqual(self.client, other)

        other = Client("2990216079954", "Cazaciuc", "Valentin")
        self.assertNotEqual(self.client, other)