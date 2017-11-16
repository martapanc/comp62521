import unittest

from comp62521.statistics import author_count

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

    def test_sole_author(self):
        '''self.assertEquals(author_count.appearing_sole("Marta", ["Marta"]), 1)
        self.assertEquals(author_count.appearing_sole("Marta",["Coco"]),0)'''
        self.assertEquals(author_count.appearing_sole("Coco",["Marta","oguz","Coco"]),0)
        self.assertEquals(author_count.appearing_sole("Coco", []), 0)
        self.assertEquals(author_count.appearing_sole("Coco",["oguz"]),0)
        '''self.assertEquals(author_count.appearing_sole("Coco",[["Coco"],["Coco"]]),2)'''
if __name__ == '__main__':
    unittest.main()
