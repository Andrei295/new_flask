
import unittest
from unittest import TestCase
from cs50 import SQL
import hashlib


data = SQL("sqlite:///C://Temp//userdata.db")



def get_name():
    user_1 = data.execute("SELECT Name FROM users WHERE Username = ?", "Andrei567")

    return user_1

def get_username():
    name = data.execute("SELECT Username FROM Users WHERE ID = ?", "3")
    return name

def get_password():
   
   return data.execute("SELECT Password FROM Users WHERE ID = ?", "3")

 
class Test_details(unittest.TestCase):
    def test_user(self):
        self.assertEqual(get_name(), [{'Name': 'Andrei'}])



    def test_info(self):
        name = get_username()
        word = get_password()
        print(f"name: {name}, word: {word}")  
        stored_hash = word[0]['Password']
        input_password = "qwerty"
        self.assertEqual(name, [{'Username': 'Andrei567'}])
        self.assertEqual(stored_hash, hashlib.md5(input_password.encode()).hexdigest())
    
    
    if __name__ == '__main__':
        unittest.main()




