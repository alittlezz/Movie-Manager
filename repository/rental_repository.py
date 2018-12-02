class RentalRepository:
    """
        Class that stores rentals

        Attributes:
            rentals(dictionary): list of rentals stored
    """
    def __init__(self):
        self.__rentals = {}

    def get_unique_id(self):
        """
            Returns the first free id in range [1, ...]

            Returns:
                int: first free index
        """
        used_ids = sorted([rental.id for rental in self.__rentals.values()])
        free_id = 1
        while free_id in used_ids:
            free_id += 1
        return free_id

    def add(self, new_rental):
        """
            Adds a new rental to repository

            Args:
                new_rental(Rental): rental to be added to repository
        """
        new_rental.id = self.get_unique_id()
        self.__rentals[new_rental.client.CNP + new_rental.movie.title] = new_rental

    def delete(self, CNP, title):
        """
            Removes a rental from repository

            Args:
                CNP(str): CNP of the client to be removed
                title(str): title of the movie to be removed
        """
        self.find(CNP, title)
        del self.__rentals[CNP + title]

    def delete_client(self, CNP):
        """
            Deletes all rentals that contains a given client

            Args:
                CNP(str): CNP of the deleted client
        """
        for rental in self.__rentals:
            if rental.client.CNP == CNP:
                self.delete(CNP, rental.movie.title)

    def update_client(self, CNP, new_client):
        """
            Updates all rentals that contains a given client

            Args:
                CNP(str): CNP of the deleted client
                new_client(Client): new value for client
        """
        for rental in self.__rentals:
            if rental.client.CNP == CNP:
                rental.client = new_client
                self.update(CNP, rental.movie.title, rental)

    def update(self, CNP, title, new_rental):
        """
            Updates a rental from repository:

            Args:
                CNP(str): CNP of the client to be updated
                title(str): title of the movie to be updated
                new_rental(Rental): new value for rental
        """
        self.delete(CNP, title)
        self.add(new_rental)

    def find(self, CNP, title):
        """
            Finds a rental from repository

            Args:
                CNP(str): CNP of the client to be searched
                title(str): title of the movie to be searched

            Raises:
                ValueError: if rental with CNP and title doesn't exist in repository
        """
        try:
            return self.__rentals[CNP + title]
        except ValueError:
            raise ValueError("Nu exista inchiere realizata de acest CNP pentru acel titlu")

    def get_all(self):
        """
            Returns list of rentals from repository

            Returns:
                list: list of rentals from repository
        """
        return list(self.__rentals.values())