from domain.client_formatter import ClientFormatter
from domain.movie_formatter import MovieFormatter


class RentalFormatter:
    """
        Class the formats the rental and it's attributes
    """
    def __init__(self):
        self.movie_formatter = MovieFormatter()
        self.client_formatter = ClientFormatter()

    def format_rental(self, rental):
        """`
            Formats rental attributes

            Args:
                rental(Rental): rental to be formatted
        """
        self.movie_formatter.format(rental.movie)
        self.client_formatter.format(rental.client)

    def format_CNP(self, CNP):
        return self.client_formatter.format_CNP(CNP)

    def format_title(self, title):
        return self.movie_formatter.format_title(title)

    def format_genre(self, genre):
        return self.movie_formatter.format_genre(genre)

    def format_client(self, client):
        self.client_formatter.format(client)

    def format_movie(self, movie):
        self.movie_formatter.format(movie)
