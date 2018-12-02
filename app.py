from service.client_service import ClientService
from service.movie_service import MovieService
from service.rental_service import RentalService
from domain.client_formatter import ClientFormatter
from domain.client_validator import ClientValidator
from domain.movie_formatter import MovieFormatter
from domain.movie_validator import MovieValidator
from domain.rental_formatter import RentalFormatter
from domain.rental_validator import RentalValidator
from repository.client_repository import ClientRepository
from repository.movie_repository import MovieRepository
from repository.rental_repository import RentalRepository
from ui.consoleUI import ConsoleUI

if __name__ == "__main__":
    movie_repository = MovieRepository()
    client_repository = ClientRepository()
    rental_repository = RentalRepository()

    client_controller = ClientService(client_repository, ClientValidator(), ClientFormatter(), rental_repository, True)
    movie_controller = MovieService(movie_repository, MovieValidator(), MovieFormatter(), True)
    rental_controller = RentalService(rental_repository, RentalValidator(), RentalFormatter(), movie_repository, client_repository, True)

    ui = ConsoleUI(client_controller, movie_controller, rental_controller)
    ui.show()