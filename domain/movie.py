import unittest

class Movie:
    """
        Class for the movie entity

        Attributes:
            id(int): unique id for the movie
            title(str): title of the movie and also a unique id
            description(str): description of the movie
            genre(str): genre of the movie
    """
    def __init__(self, title, description = None, genre = None, id = None):
        self.__id = id
        self.__title = title
        self.__description = description
        self.__genre = genre

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
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description

    @property
    def genre(self):
        return self.__genre

    @genre.setter
    def genre(self, genre):
        self.__genre = genre

    def copy(self):
        return Movie(self.title, self.description, self.genre)

    def __repr__(self):
        representation = ""
        representation += "Titlu: " + self.title + '\n'
        representation += "Descriere: " + self.description + '\n'
        representation += "Genuri: " + self.genre + '\n'
        return representation

    def __eq__(self, other):
        return self.title == other.title

    def __hash__(self):
        return hash(self.title)

class MovieDTO(Movie):
    def __init__(self, movie, no_rentals = 0):
        super().__init__(movie.title, movie.description, movie.genre, id = movie.id)
        self.__no_rentals = no_rentals

    @property
    def no_rentals(self):
        return self.__no_rentals

    @no_rentals.setter
    def no_rentals(self, no_rentals):
        self.__no_rentals = no_rentals

def get_movieDTO_data_from_list(movies):
    data = []
    data.append(["ID", "Titlu", "Descriere", "Gen", "Inchirieri"])
    for movie in movies:
        attributes = list(map(str, [movie.id, movie.title, movie.description, movie.genre, movie.no_rentals]))
        data.append(attributes)
    return data

def get_movie_data_from_list(movies):
    data = []
    data.append(["ID", "Titlu", "Descriere", "Gen"])
    for movie in movies:
        attributes = list(map(str, [movie.id, movie.title, movie.description, movie.genre]))
        data.append(attributes)
    return data

class TestMovie(unittest.TestCase):
    def test_getters(self):
        movie = Movie("T1", "D1", "G1")
        self.assertEqual(movie.title, "T1")
        self.assertEqual(movie.description, "D1")
        self.assertEqual(movie.genre, "G1")

    def test_setters(self):
        movie = Movie("T1", "D1", "G1")
        movie.title = "Titlu"
        self.assertEqual(movie.title, "Titlu")
        movie.description = "Descriere"
        self.assertEqual(movie.title, "Titlu")
        movie.genre = "Genuri"
        self.assertEqual(movie.genre, "Genuri")

    def test_eq(self):
        movie1 = Movie("T1", "G1", "D1")
        movie2 = Movie("T2", "G1", "D1")
        movie3 = Movie("T1", "G2", "D3")
        self.assertNotEqual(movie1, movie2)
        self.assertNotEqual(movie2, movie3)
        self.assertEqual(movie1, movie3)