import unittest

from service import movie_service, client_service, rental_service
from domain import movie, client, client_validator, movie_validator, client_formatter, movie_formatter, rental
from repository import base_repository, client_repository, movie_repository

if __name__ == "__main__":
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromModule(movie))
    suite.addTests(loader.loadTestsFromModule(movie_service))
    suite.addTests(loader.loadTestsFromModule(movie_validator))
    suite.addTests(loader.loadTestsFromModule(movie_formatter))
    suite.addTests(loader.loadTestsFromModule(movie_repository))

    suite.addTests(loader.loadTestsFromModule(client))
    suite.addTests(loader.loadTestsFromModule(client_service))
    suite.addTests(loader.loadTestsFromModule(client_validator))
    suite.addTests(loader.loadTestsFromModule(client_formatter))
    suite.addTests(loader.loadTestsFromModule(client_repository))

    suite.addTests(loader.loadTestsFromModule(rental))
    suite.addTests(loader.loadTestsFromModule(rental_service))

    unittest.TextTestRunner(verbosity=2).run(suite)