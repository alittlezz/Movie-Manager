from domain.client import Client, get_client_data_from_list, get_clientDTO_data_from_list
from domain.movie import Movie, get_movie_data_from_list, get_movieDTO_data_from_list
from domain.rental import get_rental_data_from_list


class Submenu:
    def __init__(self, description, tasks, tasks_description):
        self.__description = description
        self.__tasks = tasks
        self.__tasks_description = tasks_description
        self.MAX_WIDTH = 50

    def __print_tasks(self):
        for task_description in self.__tasks_description.values():
            print(task_description)

    def print_data(self, data):
        max_width = [0 for i in range(len(data[0]))]
        for i in range(len(data)):
            for j in range(len(data[i])):
                max_width[j] = min(self.MAX_WIDTH, max(max_width[j], len(data[i][j])))
                if len(data[i][j]) > self.MAX_WIDTH:
                    data[i][j] = data[i][j][:self.MAX_WIDTH] + "..."

        max_width = [width + 5 for width in max_width]
        for row in data:
            print("".join(attr.ljust(width) for attr, width in zip(row, max_width)))


    def show(self):
        self.__print_tasks()
        command = input("Introduceti comanda: ")
        try:
            result = self.__tasks[command]()
        except KeyError:
            print("!!!Comanda nu este valida")

    @property
    def description(self):
        return self.__description


class ManageMoviesSubmenu(Submenu):
    def __init__(self, movie_controller, rental_controller):
        self.__controller = movie_controller
        self._rental_controller = rental_controller
        tasks = {
            "a": self.add,
            "b": self.delete,
            "c": self.update,
            "d": self.list,
            "e": self.find,
            "f": self.generate
        }
        tasks_description = {
            "add": "a)Adauga un film nou",
            "delete": "b)Sterge un film dupa titlu",
            "update": "c)Actualizeaza un film dupa titlu",
            "list": "d)Listeaza toate filmele",
            "find": "e)Cauta film dupa titlu",
            "generate": "f)Genereaza filme"
        }
        super().__init__("Gestionare filme", tasks, tasks_description)

    @staticmethod
    def get_new_movie():
        title = input("Introduceti titlul: ")
        description = input("Introduceti descrierea: ")
        genre = input("Introduceti genurile: ")
        return Movie(title, description, genre)

    def add(self):
        new_movie = self.get_new_movie()
        self.__controller.add(new_movie)

    def delete(self):
        title = input("Introduceti titlul: ")
        self.__controller.delete(title)
        self._rental_controller.delete_movie(title)

    def update(self):
        title = input("Introduceti titlul: ")
        new_movie = self.get_new_movie()
        self.__controller.update(title, new_movie)
        self._rental_controller.update_movie(title, new_movie)

    def list(self):
        movies = self.__controller.get_list()
        self.print_data(get_movie_data_from_list(movies))

    def find(self):
        title = input("Introduceti titlul: ")
        print(self.__controller.find(title))

    def generate(self):
        n = int(input("Introduceti numarul de filme de generat: "))
        generated_movies = self.__controller.generate(n)
        for movie in generated_movies:
            print(movie)

class ManageClientsSubmenu(Submenu):
    def __init__(self, client_controller, rental_controller):
        self.__controller = client_controller
        self.__rental_controller = rental_controller
        tasks = {
            "a": self.add,
            "b": self.delete,
            "c": self.update,
            "d": self.list,
            "e": self.find
        }
        tasks_description = {
            "add": "a)Adauga un client nou",
            "delete": "b)Sterge un client dupa CNP",
            "update": "c)Actualizeaza un client dupa CNP",
            "list": "d)Listeaza toti clientii",
            "find": "e)Cauta client dupa CNP"
        }
        super().__init__("Gestionare clienti", tasks, tasks_description)

    @staticmethod
    def get_new_client():
        CNP = input("Introduceti CNP: ")
        surname = input("Introduceti nume: ")
        name = input("Introduceti prenume: ")
        return Client(CNP, surname, name)

    def add(self):
        new_client = self.get_new_client()
        self.__controller.add(new_client)

    def delete(self):
        CNP = input("Introduceti CNP: ")
        self.__controller.delete(CNP)

    def update(self):
        CNP = input("Introduceti CNP: ")
        new_client = self.get_new_client()
        self.__controller.update(CNP, new_client)

    def list(self):
        clients = self.__controller.get_list()
        self.print_data(get_client_data_from_list(clients))

    def find(self):
        CNP = input("Introduceti CNP: ")
        print(self.__controller.find(CNP))


class ManageRentalsSubmenu(Submenu):
    def __init__(self, rental_controller):
        self.__controller = rental_controller
        tasks = {
            "a": self.rent,
            "b": self.return_movie,
            "c": self.list
        }
        tasks_description = {
            "rent": "a)Inchiriaza un film",
            "return_movie": "b)Returneaza un film",
            "list": "c)Listeaza toate inchirierile"
        }
        super().__init__("Gestionare inchirieri", tasks, tasks_description)

    def rent(self):
        movie_title = input("Introduceti titlul filmului: ")
        CNP = input("Introduceti CNP: ")
        self.__controller.rent(movie_title, CNP)

    def return_movie(self):
        movie_title = input("Introduceti titlul filmului: ")
        CNP = input("Introduceti CNP: ")
        self.__controller.return_movie(movie_title, CNP)

    def list(self):
        rentals = self.__controller.get_list()
        self.print_data(get_rental_data_from_list(rentals))

class ManageStatistics(Submenu):
    def __init__(self, rental_controller):
        self.__controller = rental_controller
        tasks = {
            "a": self.clients_sorted_by_name,
            "b": self.clients_sorted_by_rentals,
            "c": self.movies_sorted_by_rentals,
            "d": self.top30_clients,
            "e": self.client_with_most_rented_genre
        }
        tasks_description = {
            "a": "a)Afiseaza clientii cu filme inchiriate sortati dupa nume",
            "b": "b)Afiseaza clientii cu filme inchiriate sortati dupa numarul de filme inchiriate",
            "c": "c)Afiseaza cele mai inchriate filme",
            "d": "d)Afiseaza primii 30% clienti cu cele mai multe filme",
            "e": "e)Afisati clientul cu cele mai multe filme inchiriate de un anumit gen"
        }
        super().__init__("Gestionare rapoarte", tasks, tasks_description)

    def clients_sorted_by_name(self):
        clients = self.__controller.clients_sorted_by_name()
        self.print_data(get_client_data_from_list(clients))

    def clients_sorted_by_rentals(self):
        clients = self.__controller.clients_sorted_by_rentals()
        self.print_data(get_clientDTO_data_from_list(clients))

    def movies_sorted_by_rentals(self):
        movies = self.__controller.movies_sorted_by_rentals()
        self.print_data(get_movieDTO_data_from_list(movies))

    def top30_clients(self):
        clients = self.__controller.top30_clients()
        self.print_data(get_clientDTO_data_from_list(clients))

    def client_with_most_rented_genre(self):
        genre = input("Introduceti genul dorit: ")
        client = self.__controller.client_with_most_rented_genre(genre)
        self.print_data(get_clientDTO_data_from_list([client]))