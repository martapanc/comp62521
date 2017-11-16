import unittest

from comp62521.statistics import author_count

class TestAverage(unittest.TestCase):

    def setUp(self):
        pass

    def test_first_appearance(self):
        self.assertEqual(author_count.appearing_first("oguz", ["oguz"]), 1)
        self.assertEqual(author_count.appearing_first("oguz", ["oguz", "a"]), 1)
        self.assertEqual(author_count.appearing_first("oguz", ["b", "oguz", "a"]), 0)
        self.assertEqual(author_count_appearing_first("oguz",["a","b","c"]),0)

    def test_last_appearance(self):
        self.assertEqual(author_count.appearing_last("oguz", ["oguz"]), 1)
        self.assertEqual(author_count.appearing_last("oguz", ["a", "oguz"]), 1)
        self.assertEqual(author_count.appearing_last("oguz", ["a", "oguz", "b"]), 0)
        self.assertEqual(author_count_appearing_last("oguz",["a","b","c"]),0)

if __name__ == '__main__':
    unittest.main()
