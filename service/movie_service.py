import random
import string

from domain.movie_formatter import MovieFormatter
from domain.movie_validator import MovieValidator
from domain.movie import Movie
import unittest

from repository.movie_repository import MovieRepository


class MovieService:
    """
        Class that handles movie events

        Attributes:
            repository(MovieRepository): where we store the movies data
            validator(MovieValidator): validates movies and their attributes
            formatter(MovieFormatter): formats the movie and their attributes
            populate(bool): flag that indicates if you should populate the repository
    """
    def __init__(self, repository, validator, formatter, populate = False):
        self.__repository = repository
        self.__validator = validator
        self.__formatter = formatter
        if populate == True:
            self.__populate_repository()

    def __populate_repository(self):
        """
            Populates the repository
        """
        self.add(Movie("The shape of water", "A movie about a girl trying to find her love. Emotional yet peaceful.", "Romance, Drama"))
        self.add(Movie("Maze runner 2", "A movie about 3 brothers trying to escape a cursed maze.", "Action, Drama, SF"))
        self.add(Movie("Now you see me", "A movie about magic. An organization founded on the premise of magic tries to make the world a better place.", "Crime, Mystery, Thriller"))
        self.add(Movie("The scorpion king", "A movie about a man trying to regain his respect among the tribe. A old but classic movie.", "Action, Adventure, Drama, Romance"))
        self.add(Movie("Unfriended", "A movie about a group of friends experiencing mysterious events. Will they survive to find the answer?", "horror"))

    def add(self, new_movie):
        """
            Adds a new movie to the database

            Args:
                new_movie(Movie): new movie to be added

            Raises:
                ValueError: if there already exists a movie with the same CNP
        """
        self.__formatter.format(new_movie)
        self.__validator.validate(new_movie)

        self.__repository.add(new_movie)

    def delete(self, title):
        """
            Deletes a movie based on title

            Args:
                title(str): unique identifier for movies
        """
        title = self.__formatter.format_title(title)
        self.__validator.validate_title(title)

        self.__repository.delete(title)

    def update(self, title, new_movie):
        """
            Updates a movie based on title

            Args:
                title(str): unique identifier for movies
                new_movie(Movie): new attributes of the old movie
        """
        title = self.__formatter.format_title(title)
        self.__validator.validate_title(title)
        self.__formatter.format(new_movie)
        self.__validator.validate(new_movie)

        self.__repository.update(title, new_movie)

    def find(self, title):
        """
            Finds a movie based on title

            Args:
                title(str): unique identified for movies

            Returns:
                Movie: movie with title equal to the given one

            Raises:
                ValueError: if there isn't any movie with the given title
        """
        title = self.__formatter.format_title(title)
        self.__validator.validate_title(title)

        return self.__repository.find(title)

    def get_list(self):
        """
            Gets list of movies

            Returns:
                list: list of movies from the database
        """
        return self.__repository.get_all()

    def generate(self, n):
        """
            Generates n random valid movies

            Args:
                n(int): number of movies to be generated

            Returns:
                list: list of random generated movies
        """
        random_movies = []
        for i in range(n):
            movie = Movie("".join(random.choices(string.ascii_lowercase + ' ', k = random.randint(2, 10))).lstrip(' '),
                          "".join(random.choices(string.ascii_lowercase + '. ', k = random.randint(10, 100))).lstrip('. '),
                          "".join(random.choices(string.ascii_lowercase + ',,, ', k = random.randint(10, 30))).lstrip(', '))
            self.__formatter.format(movie)
            self.__validator.validate(movie)
            random_movies.append(movie)
        return random_movies

class TestMovieController(unittest.TestCase):
    def setUp(self):
        self.controller = MovieService(MovieRepository(), MovieValidator(), MovieFormatter())
        self.controller.add(Movie("T1", "D1", "G1"))
        self.controller.add(Movie("T2", "D2", "G2"))
        self.controller.add(Movie("T3", "D3", "G3"))

    def test_add(self):
        self.controller.add(Movie("T4", "D4", "G4"))
        self.assertEqual(len(self.controller.get_list()), 4)
        self.assertEqual(self.controller.find("T4").id, 4)

        self.assertRaises(ValueError, self.controller.add, Movie("T5", "D5", ""))
        self.assertRaises(ValueError, self.controller.add, Movie("T5", "", ""))
        self.assertRaises(ValueError, self.controller.add, Movie("", "D5", ""))
        self.assertRaises(ValueError, self.controller.add, Movie("", "", ""))
        self.assertEqual(len(self.controller.get_list()), 4)
        self.assertRaises(ValueError, self.controller.find, "T5")

        self.assertRaises(ValueError, self.controller.add, Movie("T4", "D5", "G5"))
        self.assertEqual(len(self.controller.get_list()), 4)

    def test_get_list(self):
        self.assertEqual(len(self.controller.get_list()), 3)

    def test_delete(self):
        self.controller.delete("T2")
        self.assertEqual(len(self.controller.get_list()), 2)
        self.assertRaises(ValueError, self.controller.find, "T2")

        self.assertRaises(ValueError, self.controller.delete, "T2")

    def test_update(self):
        self.controller.update("T2", Movie("T4", "D4", "G4"))
        self.assertEqual(len(self.controller.get_list()), 3)
        self.assertRaises(ValueError, self.controller.find, "T2")
        self.assertEqual(self.controller.find("T4").id, 2)

        self.assertRaises(ValueError, self.controller.update, "T2", Movie("T5", "D5", "G5"))

    def test_find(self):
        self.assertEqual(self.controller.find("T1").id, 1)
        self.assertEqual(self.controller.find("T2").id, 2)
        self.assertEqual(self.controller.find("T3").id, 3)

    def test_generate(self):
        movies = self.controller.generate(10)
        self.assertEqual(len(movies), 10)
        for movie in movies:
            self.controller.add(movie)