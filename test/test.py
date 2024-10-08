
import unittest
from unittest import TestCase
from cs50 import SQL

data = SQL("sqlite:///C://Temp//userdata.db")

class Test(unittest.TestCase): #python -m unittest
    def test_value(self):
        self.assertEqual(value, 1)

if __name__ == '__main__':
    unittest.main()


value = data.execute("SELECT * FROM users WHERE ClassID = ?", 1)