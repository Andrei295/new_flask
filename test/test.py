
import unittest
from unittest import TestCase
from cs50 import SQL



def add(a, b):
    return a + b


class TestMath(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(add(2, 3), 5)


if __name__ == '__main__':
    unittest.main()



data = SQL("sqlite:///C://Temp//userdata.db")

def get_name(user_1):
    user_1 = data.execute("SELECT Name FROM users WHERE Username = Andrei567")

    return user_1


def adduser(user_1):
    def test_user(self):
        self.assertEqual(get_name(user_1), "Andrei")


if __name__ == '__main__':
    unittest.main()