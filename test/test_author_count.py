import unittest

from comp62521.statistics import author_count
from comp62521.statistics import author_lastname

class TestAuthorCount(unittest.TestCase):

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

#<<<<<<< HEAD
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

#=======
    def test_sole_author(self):
        '''self.assertEquals(author_count.appearing_sole("Marta", ["Marta"]), 1)
        self.assertEquals(author_count.appearing_sole("Marta",["Coco"]),0)'''
        self.assertEquals(author_count.appearing_sole("Coco",["Marta","oguz","Coco"]),0)
        self.assertEquals(author_count.appearing_sole("Coco", []), 0)
        self.assertEquals(author_count.appearing_sole("Coco",["oguz"]),0)
        '''self.assertEquals(author_count.appearing_sole("Coco",[["Coco"],["Coco"]]),2)'''
#>>>>>>> master
if __name__ == '__main__':
    unittest.main()
