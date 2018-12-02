from domain.client_validator import ClientValidator
from domain.movie_validator import MovieValidator


class RentalValidator:
    """
        Class that validates the rental and it's attributes
    """
    def __init__(self):
        self.movie_validator = MovieValidator()
        self.client_validator = ClientValidator()

    def validate_rental(self, rental):
        """
            Validate rental attributes

            Args:
                rental(Rental): rental to be validated
        """
        self.movie_validator.validate(rental.movie)
        self.client_validator.validate(rental.client)

    def validate_CNP(self, CNP):
        self.client_validator.validate_CNP(CNP)

    def validate_title(self, title):
        self.movie_validator.validate_title(title)

    def validate_genre(self, genre):
        self.movie_validator.validate_genre(genre)

    def validate_client(self, client):
        self.client_validator.validate(client)

    def validate_movie(self, movie):
        self.movie_validator.validate(movie)
