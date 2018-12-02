import unittest
import datetime

from domain.client import Client
from domain.movie import Movie


class Rental:
    """
        Class for the rental entity

        Attributes:
            id(int): unique id for the rental
            movie(Movie): movie rented
            client(Client): client which rented the movie
            rented_date(datetime): date when movie was rented
            due_date(datetime): date when movie is due to be returned
            returned_date(datetime): date when movie was returned
    """
    def __init__(self, movie, client, rented_date = datetime.date.today(), due_date = None, returned_date = None):
        self.__id = None
        self.__movie = movie
        self.__client = client
        self.__rented_date = rented_date
        self.__due_date = rented_date + datetime.timedelta(30)
        self.__returned_date = returned_date

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id
    @property
    def movie(self):
        return self.__movie

    @movie.setter
    def movie(self, new_movie):
        self.__movie = new_movie

    @property
    def client(self):
        return self.__client

    @client.setter
    def client(self, new_client):
        self.__client = new_client

    @property
    def rented_date(self):
        return self.__rented_date

    @property
    def due_date(self):
        return self.__due_date

    @property
    def returned_date(self):
        return self.__returned_date

    @returned_date.setter
    def returned_date(self, returned_date):
        if self.returned_date == None:
            self.__returned_date = returned_date
        else:
            raise Exception("Filmul a fost deja adus")

    def copy(self):
        return Rental(self.movie.copy(), self.client.copy())

    def __repr__(self):
        representation = ""
        representation += "Titlu film: " + self.movie.title + '\n'
        representation += "CNP client: " + self.client.CNP + '\n'
        representation += "Data inchiriere: " + str(self.rented_date) + '\n'
        representation += "Data limita: " + str(self.due_date) + '\n'
        if self.returned_date != None:
            representation += "Data retur: " + self.returned_date + '\n'
        else:
            representation += "Data retur: " + "inca este inchiriat" + '\n'
        return representation

    def __eq__(self, other):
        return self.movie.title == other.movie.title and self.client.CNP == other.client.CNP


def get_rental_data_from_list(rentals):
    data = []
    data.append(["ID", "CNP client", "Titlu film", "Data inchiriere", "Data scadenta", "Data returnat"])
    for rental in rentals:
        attributes = list(map(str,[rental.id, rental.client.CNP, rental.movie.title, rental.rented_date, rental.due_date, rental.returned_date]))
        data.append(attributes)
    return data

class TestRental(unittest.TestCase):
    def setUp(self):
        self.rental = Rental(Movie("T1", "D1", "G1"), Client("1990216079954", "Cazaciuc", "Valentin"))

    def test_setter(self):
        self.rental.id = 3
        self.assertEqual(self.rental.id, 3)

        self.rental.returned_date = datetime.date(2018, 11, 19)
        self.assertEqual(self.rental.returned_date, datetime.date(2018, 11, 19))

    def test_getters(self):
        self.assertEqual(self.rental.client, Client("1990216079954", "Cazaciuc", "Valentin"))
        self.assertEqual(self.rental.movie, Movie("T1", "D1", "G1"))
        self.assertEqual(self.rental.rented_date, datetime.date.today())
        self.assertEqual(self.rental.due_date, datetime.date.today() + datetime.timedelta(30))
        self.assertEqual(self.rental.returned_date, None)

    def test_eq(self):
        other = self.rental.copy()
        other.returned_date = datetime.date.today()
        self.assertEqual(self.rental, other)

        other = self.rental.copy()
        other.movie.title = "T2"
        self.assertNotEqual(self.rental, other)