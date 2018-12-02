import unittest

from domain.movie import Movie


class MovieRepository:
    """
        Class that stores movies

        Attributes:
            movies(dictionary): list of movies stored
    """
    def __init__(self):
        self.__movies = {}

    def get_unique_id(self):
        """
            Returns the first free id in range [1, ...]

            Returns:
                int: first free index
        """
        used_ids = sorted([movie.id for movie in self.__movies.values()])
        free_id = 1
        while free_id in used_ids:
            free_id += 1
        return free_id

    def add(self, new_movie):
        """
            Adds a new movie to repository

            Args:
                new_movie(Movie): movie to be added to repository

            Raises:
                ValueError: if movie with new_movie title already exists in repostiroy
        """
        try:
            self.find(new_movie.title)
            is_duplicate = True
        except ValueError:
            new_movie.id = self.get_unique_id()
            self.__movies[new_movie.title] = new_movie
            is_duplicate = False

        if is_duplicate == True:
            raise ValueError("Exista deja film cu acest titlu")

    def delete(self, title):
        """
            Removes a movie from repository

            Args:
                title(str): title of the movie to be removed
        """
        self.find(title)
        del self.__movies[title]

    def update(self, title, new_movie):
        """
            Updates a movie from repository:

            Args:
                title(str): title of the movie to be updated
                new_movie(Movie): new value for movie
        """
        self.delete(title)
        self.add(new_movie)

    def find(self, title):
        """
            Finds a movie from repository

            Args:
                title(str): title of the movie to be searched

            Raises:
                ValueError: if movie with title doesn't exist in repository
        """
        try:
            return self.__movies[title]
        except KeyError:
            raise ValueError("Nu exista film cu acest titlu")

    def get_all(self):
        """
            Returns list of movies from repository

            Returns:
                list: list of movies from repository
        """
        return list(self.__movies.values())


class TestClientRepository(unittest.TestCase):
    def setUp(self):
        self.repository = MovieRepository()

    def test_get_all(self):
        self.assertEqual(len(self.repository.get_all()), 0)
        self.repository.add(Movie("T1"))
        self.assertEqual(len(self.repository.get_all()), 1)
        self.repository.add(Movie("T2"))
        self.assertEqual(len(self.repository.get_all()), 2)

    def test_add(self):
        self.repository.add(Movie("T1"))
        self.assertEqual(len(self.repository.get_all()), 1)
        self.repository.add(Movie("T2"))
        self.assertEqual(len(self.repository.get_all()), 2)
        self.repository.add(Movie("T3"))
        self.assertEqual(len(self.repository.get_all()), 3)
        self.assertRaises(ValueError, self.repository.add, Movie("T1"))
        self.assertEqual(len(self.repository.get_all()), 3)

    def test_delete(self):
        self.repository.add(Movie("T1"))
        self.repository.add(Movie("T2"))
        self.repository.delete("T1")
        self.assertEqual(len(self.repository.get_all()), 1)
        self.assertRaises(ValueError, self.repository.delete, "T3")
        self.assertEqual(len(self.repository.get_all()), 1)

    def test_find(self):
        self.repository.add(Movie("T1"))
        self.repository.find("T1")
        self.repository.add(Movie("T2"))
        self.repository.find("T2")
        self.assertRaises(ValueError, self.repository.find, "T3")

    def test_update(self):
        self.repository.add(Movie("T1"))
        self.repository.update("T1", Movie("T2"))
        self.assertEqual(len(self.repository.get_all()), 1)
        self.repository.find("T2")
        self.assertRaises(ValueError, self.repository.find, "T1")

    def test_get_unique_id(self):
        self.assertEqual(self.repository.get_unique_id(), 1)
        self.repository.add(Movie("T1"))
        self.assertEqual(self.repository.get_unique_id(), 2)
        self.repository.add(Movie("T2"))
        self.assertEqual(self.repository.get_unique_id(), 3)
        self.repository.delete("T1")
        self.assertEqual(self.repository.get_unique_id(), 1)