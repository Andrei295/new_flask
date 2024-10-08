
import unittest
from unittest import TestCase
from cs50 import SQL


data = SQL("sqlite:///C://Temp//userdata.db")




def get_name():
    user_1 = data.execute("SELECT Name FROM users WHERE Username = ?", "Andrei567")

    return user_1

class Test_name(unittest.TestCase):
    def test_user(self):
        self.assertEqual(get_name(), [{'Name': 'Andrei'}])


if __name__ == '__main__':
    unittest.main()