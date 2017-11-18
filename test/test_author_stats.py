from os import path
import unittest

from comp62521.database import database

class TestAuthorStats(unittest.TestCase):

    def setUp(self):
        dir, _ = path.split(__file__)
        self.data_dir = path.join(dir, "..", "data")

    def test_author_stats(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_curated_sample.xml")))
        self.assertEqual(db.get_author_stats('Stefano Ceri'),(218, 100, 94, 6, 18, 230, 86, 33))
        self.assertEqual(db.get_author_stats(''), (0, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(db.get_author_stats('Xianghe'), (0, 0, 0, 0, 0, 0, 0, 0))


if __name__ == '__main__':
    unittest.main()
