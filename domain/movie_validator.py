import unittest

class MovieValidator:
    """
        Class that validates the movie and it's attributes
    """
    def validate(self, movie):
        """
            Validate movie attributes

            Args:
                movie(Movie): movie to be validated

            Raises:
                ValueError: if any of movie attributes are wrong
        """
        errors = []
        try:
            self.validate_title(movie.title)
        except ValueError as error:
            errors.append(str(error))

        try:
            self.validate_description(movie.description)
        except ValueError as error:
            errors.append(str(error))

        try:
            self.validate_genre(movie.genre)
        except ValueError as error:
            errors.append(str(error))

        if errors:
            errors.insert(0, '#' * 30)
            errors.append("#" * 30)
            raise ValueError("\n".join(errors))

    def validate_title(self, title):
        if title == "":
            raise ValueError("Titlul nu poate fi vid")

    def validate_description(self, description):
        if description == "":
            raise ValueError("Descrierea nu poate fi vida")

    def validate_genre(self, genre):
        if genre == "":
            raise ValueError("Genurile nu pot fi vide")

class TestMovieValidator(unittest.TestCase):
    def setUp(self):
        self.validator = MovieValidator()

    def test_validate_title(self):
        self.assertRaises(ValueError, self.validator.validate_title, "")

    def test_validate_description(self):
        self.assertRaises(ValueError, self.validator.validate_description, "")

    def test_validate_genre(self):
        self.assertRaises(ValueError, self.validator.validate_genre, "")