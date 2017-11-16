import unittest

from comp62521.statistics import author_count
from comp62521.statistics import author_lastname

class TestAverage(unittest.TestCase):

    def setUp(self):
        pass

    def test_first_appearance(self):
        self.assertEqual(author_count.appearing_first("oguz", ["oguz"]), 1)
        self.assertEqual(author_count.appearing_first("oguz", ["oguz", "a"]), 1)
        self.assertEqual(author_count.appearing_first("oguz", ["b", "oguz", "a"]), 0)
        self.assertEqual(author_count.appearing_first("oguz",["a","b","c"]),0)

    def test_last_appearance(self):
        self.assertEqual(author_count.appearing_last("oguz", ["oguz"]), 1)
        self.assertEqual(author_count.appearing_last("oguz", ["a", "oguz"]), 1)
        self.assertEqual(author_count.appearing_last("oguz", ["a", "oguz", "b"]), 0)
        self.assertEqual(author_count.appearing_last("oguz",["a","b","c"]),0)

    def test_author_last_name(self):
        self.assertEqual(author_lastname.get_author_last_name("Alessandro Artale"), "Artale")
        self.assertEqual(author_lastname.get_author_last_name("John H. Watson"), "Watson")
        self.assertEqual(author_lastname.get_author_last_name("Tom Marvolo Riddle"), "Riddle")
        self.assertEqual(author_lastname.get_author_last_name(""), "")

if __name__ == '__main__':
    unittest.main()
