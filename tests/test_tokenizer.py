# tests/test_tokenizer.py

import unittest
from src.preprocessing.tokenizer import Tokenizer

class TestFrenchTokenizer(unittest.TestCase):
    def setUp(self):
        self.tokenizer = Tokenizer()

    def test_basic_tokenization(self):
        text = "Le chat mange une souris."
        expected = ['le', 'chat', 'mange', 'une', 'souris']
        self.assertEqual(self.tokenizer.tokenize(text), expected)

    def test_contraction_handling(self):
        text = "L'élève s'est bien comporté."
        expected = ['le', 'élève', 'se', 'est', 'bien', 'comporté']
        self.assertEqual(self.tokenizer.tokenize(text), expected)

if __name__ == '__main__':
    unittest.main()