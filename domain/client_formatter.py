import unittest

from domain.client import Client


class ClientFormatter:
    """
        Class the formats the client and it's attributes
    """
    def format(self, client):
        """
            Formats client attributes

            Args:
                client(Client): client to be formatted
        """
        client.CNP = self.format_CNP(client.CNP)
        client.surname = self.format_surname(client.surname)
        client.name = self.format_name(client.name)

    @staticmethod
    def format_CNP(CNP):
        return CNP.strip()

    @staticmethod
    def format_surname(surname):
       return surname.strip().title()

    @staticmethod
    def format_name(name):
        return name.strip().title()

class TestClientFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = ClientFormatter()

    def test_format_CNP(self):
        self.assertEqual(self.formatter.format_CNP("  199"), "199")
        self.assertEqual(self.formatter.format_CNP("199    "), "199")
        self.assertEqual(self.formatter.format_CNP("  199   "), "199")

    def test_format_surname(self):
        self.assertEqual(self.formatter.format_surname("  cazaciuc  "), "Cazaciuc")
        self.assertEqual(self.formatter.format_surname("     CAZACIUC  "), "Cazaciuc")
        self.assertEqual(self.formatter.format_surname("     CazACiuC     "), "Cazaciuc")

    def test_format_name(self):
        self.assertEqual(self.formatter.format_surname("  valentin  "), "Valentin")
        self.assertEqual(self.formatter.format_surname("     VALENTIN  "), "Valentin")
        self.assertEqual(self.formatter.format_surname("     ValeNTiN     "), "Valentin")

    def test_format(self):
        client = Client("  1990216079954  ", " cazaCIUC", "  VALENTIN   ")
        self.formatter.format(client)
        self.assertEqual(client.CNP, "1990216079954")
        self.assertEqual(client.surname, "Cazaciuc")
        self.assertEqual(client.name, "Valentin")