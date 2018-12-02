from ui.submenu import ManageMoviesSubmenu, ManageClientsSubmenu, ManageRentalsSubmenu, ManageStatistics


class ConsoleUI:
    def __init__(self, client_controller, movie_controller, rental_controller):
        self.__is_running = True
        self.__submenus = {
            '1': ManageMoviesSubmenu(movie_controller, rental_controller),
            '2': ManageClientsSubmenu(client_controller, rental_controller),
            '3': ManageRentalsSubmenu(rental_controller),
            '4': ManageStatistics(rental_controller)
        }

    @staticmethod
    def __print_delimiter():
        print("-" * 30)

    def __print(self):
        self.__print_delimiter()
        for id, submenu in self.__submenus.items():
            print(id + '.' + submenu.description)
        print('x.Exit')
        self.__print_delimiter()

    def __exit(self):
        self.__is_running = False

    def show(self):
        while self.__is_running == True:
            self.__print()
            command = input("Introduceti comanda: ")
            if command == 'x':
                self.__exit()
            else:
                try:
                    self.__submenus[command].show()
                except KeyError:
                    print("!!!Comanda nu este valida")
                except ValueError as error:
                    print(error)