# from typing import List
import unittest
from models.provider import RegistrationForm

class TestRegistrationForm(RegistrationForm):
    def __init__(self, fullAddress: str) -> None:
        self.Address = fullAddress

class Tests(unittest.TestCase):
    def test_SerializeForm(self):
        address = 'testaddress:1234'
        form = TestRegistrationForm(address)
        expected = '{"Address": "%s"}' % (address)
        self.assertEqual(form.Serialize(), expected)

    def test_InitForm(self):
        address = 'testaddress:1234'
        string = '{"Address": "%s"}' % (address)
        expected = TestRegistrationForm(address)
        self.assertEqual(RegistrationForm(string).__dict__, expected.__dict__)

# unittest.main()