import unittest

from domain.movie import Movie


class MovieFormatter:
    """
        Class the formats the movie and it's attributes
    """
    def format(self, movie):
        """`
            Formats movie attributes

            Args:
                movie(Movie): movie to be formatted
        """
        movie.title = self.format_title(movie.title)
        movie.description = self.format_description(movie.description)
        movie.genre = self.format_genre(movie.genre)

    @staticmethod
    def format_title(title):
        return title.strip().title()

    @staticmethod
    def format_description(description):
        sentences = description.split('.')
        sentences = list(filter(lambda sentence : sentence != '', sentences))
        for i, sentence in enumerate(sentences):
            sentence = sentence.split()
            sentence = " ".join(sentence)
            sentence = sentence.capitalize()
            sentences[i] = sentence
        return ". ".join(sentences).strip()

    @staticmethod
    def format_genre(genre):
        genres = genre.split(',')
        genres = list(filter(lambda genre: genre != '', genres))
        for i, genre in enumerate(genres):
            genre = genre.split()
            genre = " ".join(genre)
            genre = genre.capitalize()
            genres[i] = genre
        return ", ".join(genres).strip()

class TestMovieFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = MovieFormatter()

    def test_format_title(self):
        self.assertEqual(self.formatter.format_title("  titlu MARE  "), "Titlu Mare")
        self.assertEqual(self.formatter.format_title("TITLU FOARTE MARE"), "Titlu Foarte Mare")
        self.assertEqual(self.formatter.format_title("tmic. Partea 2"), "Tmic. Partea 2")

    def test_format_description(self):
        self.assertEqual(self.formatter.format_description("este un film DESPRE tot ce se poate .  nu se stie. "), "Este un film despre tot ce se poate. Nu se stie.")
        self.assertEqual(self.formatter.format_description(" UN FILM CU O DESCRIERE SCURTA."), "Un film cu o descriere scurta")
        self.assertEqual(self.formatter.format_description("este.o.Descriere.FRAGMENTATA."), "Este. O. Descriere. Fragmentata")

    def test_format_genre(self):
        self.assertEqual(self.formatter.format_genre("horror, thriller, gen3"), "Horror, Thriller, Gen3")
        self.assertEqual(self.formatter.format_genre("   spatiu, foarte mult"), "Spatiu, Foarte mult")
        self.assertEqual(self.formatter.format_genre("  LA INCEPUT,    LA MIJLOC  , SI LA FINAL   "), "La inceput, La mijloc, Si la final")

    def test_format(self):
        movie = Movie(" TITLU CU CAPS   ", " o descriere.foarte simpla  . Dar cu litere MARI.", " gen, E UN FILM BUN, gen")
        self.formatter.format(movie)
        self.assertEqual(movie.title, "Titlu Cu Caps")
        self.assertEqual(movie.description, "O descriere. Foarte simpla. Dar cu litere mari")
        self.assertEqual(movie.genre, "Gen, E un film bun, Gen")