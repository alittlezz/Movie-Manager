import datetime
import unittest

from domain.client import Client, ClientDTO
from domain.movie import Movie, MovieDTO
from domain.rental import Rental
from domain.rental_formatter import RentalFormatter
from domain.rental_validator import RentalValidator
from repository.client_repository import ClientRepository
from repository.movie_repository import MovieRepository
from repository.rental_repository import RentalRepository


class RentalService:
    """
        Class that handles rental events

        Attributes:
            repository(RentalRepository): where we store the rentals data
            validator(RentalValidator): validates rentals and their attributes
            formatter(RentalFormatter): formats rentals and their attributes
            movie_repository(MovieRepository): repository for the movies
            client_repository(ClientRepository): repository for the clients
            populate(bool): flag that indicates if you should populate the repository
    """

    def __init__(self, repository, validator, formatter, movie_repository, client_repository, populate = False):
        self.__repository = repository
        self.__validator = validator
        self.__formatter = formatter
        self.__movie_repository = movie_repository
        self.__client_repository = client_repository
        if populate == True:
            self.__populate_repository()

    @property
    def movie_repository(self):
        return self.__movie_repository

    @property
    def client_repository(self):
        return self.__client_repository

    def __populate_repository(self):
        self.rent("the shape of water", "1991011070009")
        self.rent("The scorpion king", "2990223070001", rented_date = datetime.date(2018, 1, 1))
        self.return_movie("the scorpion king", "2990223070001", returned_date = datetime.date(2018, 1, 15))
        self.rent("maze runner 2", "2990223070001")

    def rent(self, movie_title, CNP, rented_date = None):
        """
            Make client identified by CNP rent a movie identified by movie_title, today

            Args:
                movie_title(str): title of the movie to be rented
                CNP(str): CNP of the client that rents
                rented_date(datetime.time): date when movie was rented by client

            Raises:
                ValueError: if movie is already rented
                            if client didn't return a rented movie
                            if client has a movie past due date
        """
        self.__validator.validate_title(movie_title)
        movie_title = self.__formatter.format_title(movie_title)
        movie = self.__movie_repository.find(movie_title)

        self.__validator.validate_CNP(CNP)
        CNP = self.__formatter.format_CNP(CNP)
        client = self.__client_repository.find(CNP)

        rentals = self.__repository.get_all()
        for rental in rentals:
            if rental.movie == movie and rental.returned_date == None:
                raise ValueError("Filmul a fost deja inchiriat")
            elif rental.client == client and rental.returned_date == None:
                raise ValueError("Clientul nu a adus un film inchiriat")
            elif rental.client == client and rental.due_date < rental.returned_date:
                raise ValueError("Clientul a intarziat cu returnarea unui film")

        if rented_date == None:
            self.__repository.add(Rental(movie, client))
        else:
            self.__repository.add(Rental(movie, client, rented_date = rented_date))

    def return_movie(self, movie_title, CNP, returned_date = datetime.date.today()):
        """
            Return movie rented by client

            Args:
                movie_title(str): title of rented movie
                CNP(str): CNP of client that rented
                returned_date(datetime.date): when he returned the movie (default is today)

            Raises:
                ValueError: if movie was already rented
                            if movie was not rented at all

            Returns:
                bool: True if the return was successful
        """
        self.__validator.validate_title(movie_title)
        movie_title = self.__formatter.format_title(movie_title)
        movie = self.__movie_repository.find(movie_title)

        self.__validator.validate_CNP(CNP)
        CNP = self.__formatter.format_CNP(CNP)
        client = self.__client_repository.find(CNP)

        rentals = self.__repository.get_all()
        for rental in rentals:
            if rental.movie == movie and rental.client == client:
                if rental.returned_date == None:
                    rental.returned_date = returned_date
                    self.__repository.update(rental.client.CNP, rental.movie.title, rental)
                    return True
                else:
                    raise ValueError("Filmul a fost deja returnat")

        raise ValueError("Filmul nu a fost inchiriat")

    def delete_movie(self, movie_title):
        """
            Deletes all rentals that contains a given movie

            Args:
                movie_title(str): title of the deleted movie
        """
        self.__validator.validate_title(movie_title)
        movie_title = self.__formatter.format_title(movie_title)

        for rental in self.__repository.get_all():
            if rental.movie.title == movie_title:
                self.__repository.delete(rental.client.CNP, movie_title)

    def update_movie(self, movie_title, new_movie):
        """
            Updates all rentals that contains a given movie

            Args:
                movie_title(str): title of the updated movie
                new_movie(Movie): new value for the movie
        """
        self.__validator.validate_title(movie_title)
        movie_title = self.__formatter.format_title(movie_title)

        self.__validator.validate_movie(new_movie)
        self.__formatter.format_movie(new_movie)

        for rental in self.__repository.get_all():
            if rental.movie.title == movie_title:
                rental.movie = new_movie
                self.__repository.update(rental.client.CNP, movie_title, rental)

    def clients_sorted_by_name(self):
        """
            Returns list of clients that have rentals sorted by name

            Returns:
                list: list of clients that have rentals sorted by name
        """
        rentals = self.get_list()
        rentals = sorted(rentals, key = lambda rental: rental.client.full_name)
        return [rental.client for rental in rentals]

    def clients_sorted_by_rentals(self):
        """
            Returns list of clients that have rentals sorted by number of rentals

            Returns:
                list: list of clients that have rentals sorted by number of rentals
        """
        rentals = self.get_list()
        number_of_rented_movies = dict.fromkeys([rental.client for rental in rentals], 0)
        for rental in rentals:
            number_of_rented_movies[rental.client] += 1
        items = sorted(number_of_rented_movies.items(), key = lambda item: item[1], reverse=True)
        return [ClientDTO(item[0], item[1]) for item in items]

    def movies_sorted_by_rentals(self):
        """
            Returns list of movies that have rentals sorted by number of rentals

            Returns:
                list: list of movies that have rentals sorted by number of rentals
        """
        rentals = self.get_list()
        number_of_rentals = dict.fromkeys([rental.movie for rental in rentals], 0)
        for rental in rentals:
            number_of_rentals[rental.movie] += 1
        items = sorted(number_of_rentals.items(), key = lambda item: item[1], reverse=True)
        return [MovieDTO(item[0], item[1]) for item in items]

    def top30_clients(self):
        """
            Returns top 30% clients that have rentals sorted by number of rentals

            Returns:
                list: list of top 30% clients that have rentals sorted by number of rentals
        """
        clients = self.clients_sorted_by_rentals()
        return clients[:int(0.3 * len(clients))]

    def client_with_most_rented_genre(self, genre):
        """
            Returns the client with the most rented movies of a certain genre

            Args:
                genre(str): genre of the movies to be searched

            Returns:
                Client: client with the most rented movies of a certain genre
        """
        self.__validator.validate_genre(genre)
        genre = self.__formatter.format_genre(genre)

        rentals = self.get_list()
        number_of_rented_movies_genre = dict.fromkeys([rental.client for rental in rentals], 0)
        for rental in rentals:
            if genre in rental.movie.genre:
                number_of_rented_movies_genre[rental.client] += 1
        clients = []
        for client, rentals in number_of_rented_movies_genre.items():
            clients.append(ClientDTO(client, rentals))
        client = sorted(clients, key = lambda client: client.no_rentals, reverse=True)[0]
        if client.no_rentals == 0:
            raise ValueError("Nu exista clienti care sa fi inchiriat filme avand genul " + str(genre))
        return client

    def get_list(self):
        """
            Returns list of rentals

            Returns:
                list: list of rentals
        """
        return self.__repository.get_all()


class TestClientController(unittest.TestCase):
    def setUp(self):
        self.controller = RentalService(RentalRepository(), RentalValidator(), RentalFormatter(), MovieRepository(),
                                        ClientRepository())
        self.controller.movie_repository.add(Movie("T1", "D1", "G1, G2"))
        self.controller.movie_repository.add(Movie("T2", "D2", "G2"))
        self.controller.movie_repository.add(Movie("T3", "D3", "G3, G2"))

        self.controller.client_repository.add(Client("1990216070099", "Cazaciuc", "Valentin"))
        self.controller.client_repository.add(Client("2990216070099", "Caza", "Vale"))

    def test_rent(self):
        self.controller.rent("T1", "1990216070099")
        self.assertRaises(ValueError, self.controller.rent, "T1", "2990216070099")
        self.assertRaises(ValueError, self.controller.rent, "T1", "1990216070099")
        self.controller.return_movie("T1", "1990216070099", datetime.date.today() - datetime.timedelta(1))

    def test_return_movie(self):
        self.controller.rent("T1", "1990216070099")
        lst = self.controller.get_list()[0]
        self.controller.return_movie("T1", "1990216070099")
        self.assertRaises(ValueError, self.controller.return_movie, "T1", "1990216070099")
        self.assertRaises(ValueError, self.controller.return_movie, "T2", "1990216070099")

    def test_get_list(self):
        self.assertEqual(len(self.controller.get_list()), 0)
        self.controller.rent("T1", "1990216070099")
        self.assertEqual(len(self.controller.get_list()), 1)

    def test_client_with_most_rented_genre(self):
        self.controller.rent("T1", "1990216070099")
        self.controller.rent("T2", "2990216070099", rented_date = datetime.date(2018, 1, 1))
        self.controller.return_movie("T2", "2990216070099", returned_date=  datetime.date(2018, 1, 15))
        self.controller.rent("T3", "2990216070099")
        self.assertEqual(self.controller.client_with_most_rented_genre("G1").CNP, "1990216070099")
        self.assertEqual(self.controller.client_with_most_rented_genre("G2").CNP, "2990216070099")
        self.assertRaises(ValueError, self.controller.client_with_most_rented_genre, "G4")