from os import path
import unittest

from comp62521.database import database

class TestDatabase(unittest.TestCase):

    def setUp(self):
        dir, _ = path.split(__file__)
        self.data_dir = path.join(dir, "..", "data")

    def test_read(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        self.assertEqual(len(db.publications), 1)

    def test_read_invalid_xml(self):
        db = database.Database()
        self.assertFalse(db.read(path.join(self.data_dir, "invalid_xml_file.xml")))

    def test_read_missing_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "missing_year.xml")))
        self.assertEqual(len(db.publications), 0)

    def test_read_missing_title(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "missing_title.xml")))
        # publications with missing titles should be added
        self.assertEqual(len(db.publications), 1)

    def test_get_average_authors_per_publication(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-1.xml")))
        _, data = db.get_average_authors_per_publication(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 2.3, places=1)
        _, data = db.get_average_authors_per_publication(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 2, places=1)
        _, data = db.get_average_authors_per_publication(database.Stat.MODE)
        self.assertEqual(data[0], [2])

    def test_get_average_publications_per_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-2.xml")))
        _, data = db.get_average_publications_per_author(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 1.5, places=1)
        _, data = db.get_average_publications_per_author(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 1.5, places=1)
        _, data = db.get_average_publications_per_author(database.Stat.MODE)
        self.assertEqual(data[0], [0, 1, 2, 3])

    def test_get_average_publications_in_a_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-3.xml")))
        _, data = db.get_average_publications_in_a_year(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 2.5, places=1)
        _, data = db.get_average_publications_in_a_year(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 3, places=1)
        _, data = db.get_average_publications_in_a_year(database.Stat.MODE)
        self.assertEqual(data[0], [3])

    def test_get_average_authors_in_a_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-4.xml")))
        _, data = db.get_average_authors_in_a_year(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 2.8, places=1)
        _, data = db.get_average_authors_in_a_year(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 3, places=1)
        _, data = db.get_average_authors_in_a_year(database.Stat.MODE)
        self.assertEqual(data[0], [0, 2, 4, 5])
        # additional test for union of authors
        self.assertEqual(data[-1], [0, 2, 4, 5])

    def test_get_publication_summary(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_publication_summary()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data[0]), 6,
            "incorrect number of columns in data")
        self.assertEqual(len(data), 2,
            "incorrect number of rows in data")
        self.assertEqual(data[0][1], 1,
            "incorrect number of publications for conference papers")
        self.assertEqual(data[1][1], 2,
            "incorrect number of authors for conference papers")

    def test_get_average_authors_per_publication_by_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "three-authors-and-three-publications.xml")))
        header, data = db.get_average_authors_per_publication_by_author(database.Stat.MEAN)
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 3,
            "incorrect average of number of conference papers")
        self.assertEqual(data[0][1], 1.5,
            "incorrect mean journals for author1")
        self.assertEqual(data[1][1], 2,
            "incorrect mean journals for author2")
        self.assertEqual(data[2][1], 1,
            "incorrect mean journals for author3")

    def test_get_publications_by_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_publications_by_author()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 2,
            "incorrect number of authors")
        self.assertEqual(data[0][-1], 1,
            "incorrect total")

    def test_get_average_publications_per_author_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_average_publications_per_author_by_year(database.Stat.MEAN)
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
            "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
            "incorrect year in result")

    def test_get_publications_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_publications_by_year()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
            "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
            "incorrect year in result")

    def test_get_author_totals_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_author_totals_by_year()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
            "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
            "incorrect year in result")
        self.assertEqual(data[0][1], 2,
            "incorrect number of authors in result")


    def test_get_authors_count_for_one_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_curated_sample.xml")))
        self.assertEqual(db.get_authors_count_for_one_author("Aldo Bongio", 1980, 2013, 4), [2, 2, 0])
        self.assertEqual(db.get_authors_count_for_one_author("Alon Y. Halevy", 1995, 2008, 1), [4, 10, 6])
        self.assertEqual(db.get_authors_count_for_one_author("Suzanne M. Embury", 1998, 2005, 3), [1, 1, 0])
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-4.xml")))
        self.assertEqual(db.get_authors_count_for_one_author("AUTHOR1", 2010, 2013, 4), [1, 0, 2])

    def test_search_authors(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_curated_sample.xml")))
        self.assertEqual(db.search_authors("kell"), ["Douglas B. Kell", "Arthur M. Keller", "Simon J. Cockell", "Simon J. Gaskell", "Rizos Sakellariou"])
        self.assertEqual(db.search_authors("pol"), ["Jeff Pollock", "Luigi Palopoli", "Paola Spoletini"])

    def test_search_authors_2(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "extended_author.xml")))
        self.assertEqual(db.search_authors(""), [])
        self.assertEqual(db.search_authors("sam"), ["Alice Sam", "Alice Sammer", "Sam Brian", "Samuel Brian", "Alice Sam Brian", "Alice Sammmer Brian", "Alice Alice Sam Brian", "Alice Alice Sammmer Brian", "Alice Alice Brian Sam Brian", "Alice Alice Brian Sammmer Brian", "Alice Esam"])

    def test_get_degrees_of_separation(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_sorting_example.xml")))
        self.assertEqual(db.get_degrees_of_separation("AnHai Doan", "Pedro Domingos"), 0)
        self.assertEqual(db.get_degrees_of_separation("Natalya Fridman Noy", "Pedro Domingos"), 1)

    def test_get_degrees_of_separation_2(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_sorting_example_copy.xml")))

        self.assertEqual(db.get_degrees_of_separation("Oguz Ongun", "Rafet Ongun"), 0)
        self.assertEqual(db.get_degrees_of_separation("Pedro Domingos", "Rafet Ongun"), 1)
        self.assertEqual(db.get_degrees_of_separation("Natalya Fridman Noy", "Rafet Ongun"), 3)
        self.assertEqual(db.get_degrees_of_separation("Natalya Fridman Noy", "Oguz Ongun"), 2)
        self.assertEqual(db.get_degrees_of_separation("Natalya Fridman Noy", "Justin Bieber"), 'X')
        self.assertEqual(db.get_degrees_of_separation("Oguz Ongun", "Justin Bieber"), 'X')
        self.assertEqual(db.get_degrees_of_separation("Justin Bieber", "Oguz Ongun"), 'X')
        self.assertEqual(db.get_degrees_of_separation("Justin Bieber", "Justin Bieber"), 'X')


    def test_get_2_authors_nw(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_sorting_example_copy.xml")))
        self.assertEqual(db.get_2_authors_nw(0, 8), ({0: "Alon Y. Halevy", 8: "Justin Bieber"}, []))
        self.assertEqual(db.get_2_authors_nw(1, 8), ({1: "AnHai Doan", 8: "Justin Bieber"}, []))
        self.assertEqual(db.get_2_authors_nw(8, 1), ({1: "AnHai Doan", 8: "Justin Bieber"}, []))
        self.assertEqual(db.get_2_authors_nw(0, 0), ({0: "Alon Y. Halevy"}, []))
        self.assertEqual(db.get_2_authors_nw(6, 5), ({0: "Alon Y. Halevy", 1: "AnHai Doan", 3: "Pedro Domingos", 5: "Natalya Fridman Noy", 6: "Oguz Ongun"}, [[6, 3], [3, 1], [1, 5], [3, 0], [0, 5]]))
        self.assertEqual(db.get_2_authors_nw(5, 6), ({0: "Alon Y. Halevy", 1: "AnHai Doan", 3: "Pedro Domingos", 5: "Natalya Fridman Noy", 6: "Oguz Ongun"}, [[5, 1], [1, 3], [3, 6], [5, 0], [0, 3]]))


if __name__ == '__main__':
    unittest.main()
