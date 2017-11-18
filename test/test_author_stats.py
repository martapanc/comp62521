from os import path
import unittest

from comp62521.database import database

class TestAuthorStats(unittest.TestCase):

    def setUp(self):
        pass

    def test_author_stats(self):
        self.assertEqual(author_stats.get_author_stats('Stefano Ceri'),(218, 100, 94, 6, 18, 230, 86, 33))



if __name__ == '__main__':
    unittest.main()
