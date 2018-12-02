import unittest

class ClientValidator:
    """
        Class that validates the client and it's attributes
    """
    def validate(self, client):
        """
            Validate client attributes

            Args:
                client(Client): client to be validated

            Raises:
                ValueError: if any of client attributes are wrong
        """
        errors = []
        try:
            self.validate_CNP(client.CNP)
        except ValueError as error:
            errors.append(str(error))

        try:
            self.validate_surname(client.surname)
        except ValueError as error:
            errors.append(str(error))

        try:
            self.validate_name(client.name)
        except ValueError as error:
            errors.append(str(error))

        if errors:
            errors.insert(0, '#' * 30)
            errors.append('#' * 30)
            raise ValueError("\n".join(errors))

    @staticmethod
    def validate_CNP(CNP):
        if CNP == "":
            raise ValueError("CNP-ul nu poate fi vid")
        if CNP.isdigit() == False:
            raise ValueError("CNP-ul nu poate contine alte caractere inafara de cifre")
        if len(CNP) != 13:
            raise ValueError("CNP-ul trebuie sa aibe 13 cifre")

    @staticmethod
    def validate_surname(surname):
        if surname == "":
            raise ValueError("Numele nu poate fi vid")
        if surname.isalpha() == False:
            raise ValueError("Numele nu poate sa contina altceva inafara de litere")

    @staticmethod
    def validate_name(name):
        if name == "":
            raise ValueError("Prenumele nu poate fi vid")
        if name.isalpha() == False:
            raise ValueError("Prenumele nu poate sa contina altceva inafara de litere")

    @staticmethod
    def validate_username(username):
        """
            Validates username of client

            Args:
                username(str): username to be validated

            Returns:
                bool: True if username is valid

            Raises:
                ValueError: if username is not valid
        """
        if username == "":
            return True

        cnt = 0
        for ch in username:
            if ch == ' ':
                cnt += 1
        if cnt > 1:
            raise ValueError("Username nu poate fi mai mult de 1 spatiu")

        if username[0] == ' ' or username[-1] == ' ':
            raise ValueError("Username nu se poate termina in spatiu")
        elif username[0].islower() == False:
            raise ValueError("Username nu poate incepe cu altceva inafara de litere mica")

        for i,  ch in enumerate(username):
            if ch == ' ':
                if username[i + 1].islower() == False:
                    raise ValueError("Username nu poate incepe cu altceva infara de litera mica")
            elif ch.isalpha() == False and ('0' <= ch <= '9') == False:
                raise ValueError("Username nu poate contine semne")
        return True

class TestClientValidator(unittest.TestCase):
    def setUp(self):
        self.validator = ClientValidator()

    def test_validate_CNP(self):
        self.assertRaises(ValueError, self.validator.validate_CNP, "19902160700999")
        self.assertRaises(ValueError, self.validator.validate_CNP, "199021607009")
        self.assertRaises(ValueError, self.validator.validate_CNP, "199021607009f")
        self.assertRaises(ValueError, self.validator.validate_CNP, "199021607009.9")
        self.assertRaises(ValueError, self.validator.validate_CNP, "unudoitreipatru")

    def test_validate_surname(self):
        self.assertRaises(ValueError, self.validator.validate_surname, "")
        self.assertRaises(ValueError, self.validator.validate_surname, "Cazaciuc ")
        self.assertRaises(ValueError, self.validator.validate_surname, "  Cazaciuc ")
        self.assertRaises(ValueError, self.validator.validate_surname, "cazaciuc23")
        self.assertRaises(ValueError, self.validator.validate_surname, "cazaciuc.")

    def test_validate_name(self):
        self.assertRaises(ValueError, self.validator.validate_name, "")
        self.assertRaises(ValueError, self.validator.validate_name, "Cazaciuc ")
        self.assertRaises(ValueError, self.validator.validate_name, "  Cazaciuc ")
        self.assertRaises(ValueError, self.validator.validate_name, "cazaciuc23")
        self.assertRaises(ValueError, self.validator.validate_name, "cazaciuc.")

    def test_validate_username(self):
        self.assertRaises(ValueError, self.validator.validate_username, "aNa72 ")
        self.assertRaises(ValueError, self.validator.validate_username, "Ana")
        self.assertRaises(ValueError, self.validator.validate_username, "aNa2Tp A")
        self.assertRaises(ValueError, self.validator.validate_username, "a~N")
        self.assertRaises(ValueError, self.validator.validate_username, "aN  7")
        self.assertRaises(ValueError, self.validator.validate_username, "aN  b")
        self.assertRaises(ValueError, self.validator.validate_username, "aNa aN ")
        self.assertRaises(ValueError, self.validator.validate_username, "aN aN an")

        self.assertEqual(self.validator.validate_username('ana'), True)
        self.assertEqual(self.validator.validate_username('aNa7'), True)
        self.assertEqual(self.validator.validate_username('aNa2Tp a'), True)
        self.assertEqual(self.validator.validate_username('aN a3'), True)