import unittest
from os import path

from comp62521.statistics import author_count
from comp62521.statistics import author_lastname
from comp62521.database import database

class TestAuthorCount(unittest.TestCase):

    def setUp(self):
        dir, _ = path.split(__file__)
        self.data_dir = path.join(dir, "..", "data")

    def test_first_appearance(self):
        self.assertEqual(author_count.appearing_first("oguz", ["oguz"]), 0)
        self.assertEqual(author_count.appearing_first("oguz", ["oguz", "a"]), 1)
        self.assertEqual(author_count.appearing_first("oguz", ["b", "oguz", "a"]), 0)
        self.assertEqual(author_count.appearing_first("oguz",["a","b","c"]),0)

    def test_first_appearance_for_lists(self):
        self.assertEqual(author_count.appearing_first_for_lists("oguz", [["oguz"], ["oguz", "a"], ["b", "oguz", "a"], ["a","b","c"]]), 1)
        self.assertEqual(author_count.appearing_first_for_lists("k", [["oguz"], ["oguz", "a"], ["b", "oguz", "a"], ["a","b","c"]]), 0)
        self.assertEqual(author_count.appearing_first_for_lists("k", [["oguz"], ["k", "oguz", "a"], ["b", "oguz", "a"], ["a","b","c"]]), 1)

    def test_last_appearance(self):
        self.assertEqual(author_count.appearing_last("oguz", ["oguz"]), 0)
        self.assertEqual(author_count.appearing_last("oguz", ["a", "oguz"]), 1)
        self.assertEqual(author_count.appearing_last("oguz", ["a", "oguz", "b"]), 0)
        self.assertEqual(author_count.appearing_last("oguz",["a","b","c"]),0)

    def test_last_appearance_for_lists(self):
        self.assertEqual(author_count.appearing_last_for_lists("oguz", [["oguz"], ["oguz", "a"], ["b", "a", "oguz"], ["a","b","c"]]), 1)
        self.assertEqual(author_count.appearing_last_for_lists("k", [["oguz"], ["oguz", "a"], ["b", "oguz", "a"], ["a","b","c"]]), 0)
        self.assertEqual(author_count.appearing_last_for_lists("k", [["k"], ["oguz", "a"], ["b", "oguz", "a"], ["a","b","c"]]), 0)

    def test_author_last_name(self):
        self.assertEqual(author_lastname.get_author_last_name("Alessandro Artale"), "Artale")
        self.assertEqual(author_lastname.get_author_last_name("John H. Watson"), "Watson")
        self.assertEqual(author_lastname.get_author_last_name("Tom Marvolo Riddle"), "Riddle")
        self.assertEqual(author_lastname.get_author_last_name("Nostradamus"), "Nostradamus")
        self.assertEqual(author_lastname.get_author_last_name(""), -1)

    def test_author_last_name_first(self):
        self.assertEqual(author_lastname.get_last_name_first("Alessandro Artale"), "Artale, Alessandro")
        self.assertEqual(author_lastname.get_last_name_first("John H. Watson"), "Watson, John H.")
        self.assertEqual(author_lastname.get_last_name_first("Tom Marvolo Riddle"), "Riddle, Tom Marvolo")
        self.assertEqual(author_lastname.get_last_name_first("William Sherlock Scott Holmes"), "Holmes, William Sherlock Scott")
        self.assertEqual(author_lastname.get_last_name_first("Nostradamus"), "Nostradamus")
        self.assertEqual(author_lastname.get_last_name_first(""), -1)
        self.assertEqual(author_lastname.get_last_name_first(" "), -1)
        self.assertEqual(author_lastname.get_last_name_first(" 326"), -1)
        self.assertEqual(author_lastname.get_last_name_first("John 001 Doe"), "Doe, John")
        self.assertEqual(author_lastname.get_last_name_first("John 001 Doe 1234"), "Doe, John")

    def test_sole_author(self):
        self.assertEqual(author_count.appearing_sole("Marta", ["Marta"]), 1)
        self.assertEqual(author_count.appearing_sole("Marta",["Coco"]),0)
        self.assertEqual(author_count.appearing_sole("Coco",["Marta","oguz","Coco"]),0)
        self.assertEqual(author_count.appearing_sole("Coco", []), 0)
        self.assertEqual(author_count.appearing_sole("Coco",["oguz"]),0)

    def test_sole_appearance_for_lists(self):
        self.assertEqual(author_count.appearing_sole_for_lists("oguz", [["oguz"], ["oguz", "a"], ["b", "oguz", "a"], ["a","b","c"]]), 1)
        self.assertEqual(author_count.appearing_sole_for_lists("k", [["oguz"], ["oguz", "a"], ["b", "oguz", "a"], ["a","b","c"]]), 0)
        self.assertEqual(author_count.appearing_sole_for_lists("k", [["k"], ["oguz", "a"], ["b", "oguz", "a"], ["a","b","c"], ["k"]]), 2)
        self.assertEqual(author_count.appearing_sole_for_lists("Coco",[["Coco"],["Coco"]]),2)

    def test_author_stats(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_curated_sample.xml")))
        self.assertEqual(db.get_author_stats('Stefano Ceri'),(True, 218, 100, 94, 6, 18, 230, 78, 25, u'Stefano Ceri'))
        self.assertEqual(db.get_author_stats(''), (False, 0, 0, 0, 0, 0, 0, 0, 0, ''))
        self.assertEqual(db.get_author_stats('Xianghe'), (False, 0, 0, 0, 0, 0, 0, 0, 0, ''))

if __name__ == '__main__':
    unittest.main()
