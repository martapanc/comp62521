from comp62521.statistics import average
from comp62521.statistics import author_count
from comp62521.statistics import author_lastname

import itertools
import numpy as np
from xml.sax import handler, make_parser, SAXException

PublicationType = [
    "Conference Paper", "Journal", "Book", "Book Chapter"]

class Publication:
    CONFERENCE_PAPER = 0
    JOURNAL = 1
    BOOK = 2
    BOOK_CHAPTER = 3

    def __init__(self, pub_type, title, year, authors):
        self.pub_type = pub_type
        self.title = title
        if year:
            self.year = int(year)
        else:
            self.year = -1
        self.authors = authors

class Author:
    def __init__(self, name):
        self.name = name

class Stat:
    STR = ["Mean", "Median", "Mode"]
    FUNC = [average.mean, average.median, average.mode]
    MEAN = 0
    MEDIAN = 1
    MODE = 2

class Database:
    def read(self, filename):
        self.publications = []
        self.authors = []
        self.author_idx = {}
        self.min_year = None
        self.max_year = None

        handler = DocumentHandler(self)
        parser = make_parser()
        parser.setContentHandler(handler)
        infile = open(filename, "r")
        valid = True
        try:
            parser.parse(infile)
        except SAXException as e:
            valid = False
            print ("Error reading file (" + e.getMessage() + ")")
        infile.close()

        for p in self.publications:
            if self.min_year == None or p.year < self.min_year:
                self.min_year = p.year
            if self.max_year == None or p.year > self.max_year:
                self.max_year = p.year

        return valid

    def get_all_authors(self):
        return self.author_idx.keys()

    def get_coauthor_data(self, start_year, end_year, pub_type):
        coauthors = {}
        for p in self.publications:
            if ((start_year == None or p.year >= start_year) and
                (end_year == None or p.year <= end_year) and
                (pub_type == 4 or pub_type == p.pub_type)):
                for a in p.authors:
                    for a2 in p.authors:
                        if a != a2:
                            try:
                                coauthors[a].add(a2)
                            except KeyError:
                                coauthors[a] = set([a2])
        def display(db, coauthors, author_id):
            return "%s (%d)" % (db.authors[author_id].name, len(coauthors[author_id]))

        header = ("Author", "Co-Authors")
        data = []
        for a in coauthors:
            data.append([ display(self, coauthors, a),
                ", ".join([
                    display(self, coauthors, ca) for ca in coauthors[a] ]) ])

        return (header, data)


    def get_authors_for_nw(self):
        authors = {}
        coauthors = []
        for p in self.publications:
            for a in p.authors:
                authors[a] = self.authors[a].name
                for a2 in p.authors:
                    if a != a2 and not [a,a2] in coauthors and not [a2,a] in coauthors:
                        coauthors.append([a,a2])
        return authors, coauthors


    def get_average_authors_per_publication(self, av):
        header = ("Conference Paper", "Journal", "Book", "Book Chapter", "All Publications")

        auth_per_pub = [[], [], [], []]

        for p in self.publications:
            auth_per_pub[p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [ func(auth_per_pub[i]) for i in np.arange(4) ] + [ func(list(itertools.chain(*auth_per_pub))) ]
        return (header, data)

    def get_average_publications_per_author(self, av):
        header = ("Conference Paper", "Journal", "Book", "Book Chapter", "All Publications")

        pub_per_auth = np.zeros((len(self.authors), 4))

        for p in self.publications:
            for a in p.authors:
                pub_per_auth[a, p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [ func(pub_per_auth[:, i]) for i in np.arange(4) ] + [ func(pub_per_auth.sum(axis=1)) ]
        return (header, data)

    def get_average_publications_in_a_year(self, av):
        header = ("Conference Paper",
            "Journal", "Book", "Book Chapter", "All Publications")

        ystats = np.zeros((int(self.max_year) - int(self.min_year) + 1, 4))

        for p in self.publications:
            ystats[p.year - self.min_year][p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [ func(ystats[:, i]) for i in np.arange(4) ] + [ func(ystats.sum(axis=1)) ]
        return (header, data)

    def get_average_authors_in_a_year(self, av):
        header = ("Conference Paper",
            "Journal", "Book", "Book Chapter", "All Publications")

        yauth = [ [set(), set(), set(), set(), set()] for _ in range(int(self.min_year), int(self.max_year) + 1) ]

        for p in self.publications:
            for a in p.authors:
                yauth[p.year - self.min_year][p.pub_type].add(a)
                yauth[p.year - self.min_year][4].add(a)

        ystats = np.array([ [ len(S) for S in y ] for y in yauth ])

        func = Stat.FUNC[av]

        data = [ func(ystats[:, i]) for i in np.arange(5) ]
        return (header, data)

    def get_publication_summary_average(self, av):
        header = ("Details", "Conference Paper",
            "Journal", "Book", "Book Chapter", "All Publications")

        pub_per_auth = np.zeros((len(self.authors), 4))
        auth_per_pub = [[], [], [], []]

        for p in self.publications:
            auth_per_pub[p.pub_type].append(len(p.authors))
            for a in p.authors:
                pub_per_auth[a, p.pub_type] += 1

        name = Stat.STR[av]
        func = Stat.FUNC[av]

        data = [
            [name + " authors per publication"]
                + [ func(auth_per_pub[i]) for i in np.arange(4) ]
                + [ func(list(itertools.chain(*auth_per_pub))) ],
            [name + " publications per author"]
                + [ func(pub_per_auth[:, i]) for i in np.arange(4) ]
                + [ func(pub_per_auth.sum(axis=1)) ] ]
        return (header, data)

    def get_publication_summary(self):
        header = ("Details", "Conference Paper",
            "Journal", "Book", "Book Chapter", "Total")

        plist = [0, 0, 0, 0]
        alist = [set(), set(), set(), set()]

        for p in self.publications:
            plist[p.pub_type] += 1
            for a in p.authors:
                alist[p.pub_type].add(a)
        # create union of all authors
        ua = alist[0] | alist[1] | alist[2] | alist[3]

        data = [
            ["No. of publications"] + plist + [sum(plist)],
            ["No. of authors"] + [ len(a) for a in alist ] + [len(ua)] ]
        return (header, data)

    def get_average_authors_per_publication_by_author(self, av):
        header = ("Author", "No. of conference papers",
            "No. of journals", "Number of books",
            "No. of book chapers", "All publications")

        astats = [ [[], [], [], []] for _ in range(len(self.authors)) ]
        for p in self.publications:
            for a in p.authors:
                astats[a][p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [ [ author_lastname.get_last_name_first(self.authors[i].name) ]
            + [ func(L) for L in astats[i] ]
            + [ func(list(itertools.chain(*astats[i]))) ]
            for i in range(len(astats)) ]
        return (header, data)


    def get_publications_by_author(self):
        header = ("", "Author", "No. of conference papers",
            "No. of journals", "No. of books",
            "No. of book chapers", "Total")

        astats = [ [0, 0, 0, 0] for _ in range(len(self.authors)) ]
        for p in self.publications:
            for a in p.authors:
                astats[a][p.pub_type] += 1

        data = [ [self.authors[i].name] + [author_lastname.get_last_name_first(self.authors[i].name)] + astats[i] + [sum(astats[i])]
            for i in range(len(astats)) ]
        return (header, data)

    def get_all_details_of_authors(self):
        header = ("Author", "Overall no. of publications", "No. of conference papers",
            "No. of journals", "No. of books",
            "No. of book chapers", "No. of co-authors", "No. of times appears first", "No. of times appears last", "No. of times appears sole")

        astats = [ [0, 0, 0, 0] for _ in range(len(self.authors)) ]
        astats2 = [ [0, 0, 0, 0] for _ in range(len(self.authors)) ]
        coauthors = {}
        for p in self.publications:
            for a in p.authors:
                astats[a][p.pub_type] += 1
                astats2[a][1] += author_count.appearing_first(a, p.authors)
                astats2[a][2] += author_count.appearing_last(a, p.authors)
                astats2[a][3] += author_count.appearing_sole(a, p.authors)
                for a2 in p.authors:
                        if a != a2:
                            try:
                                coauthors[a].add(a2)
                            except KeyError:
                                coauthors[a] = set([a2])
        for p in self.publications:
            for a in p.authors:
                try:
                    astats2[a][0] = len(coauthors[a])
                except:
                    astats2[a][0] = 0
        data = [ [ author_lastname.get_last_name_first(self.authors[i].name) ] + [sum(astats[i])] + astats[i] + astats2[i]
            for i in range(len(astats)) ]
        return (header, data)

    def get_authors_count(self, start_year, end_year, pub_type):
        header = ("Author", "No. of times the author appears first",
            "No. of times the author appears last","No. of times the author appears sole")

        astats = [ [0, 0, 0] for _ in range(len(self.authors)) ]
        for p in self.publications:
            if ( (start_year == None or p.year >= start_year) and
                (end_year == None or p.year <= end_year) and
                (pub_type == 4 or pub_type == p.pub_type) ):
                for a in p.authors:
                    astats[a][0] += author_count.appearing_first(a, p.authors)
                    astats[a][1] += author_count.appearing_last(a, p.authors)

                    astats[a][2] += author_count.appearing_sole(a, p.authors)
        data = [ [self.authors[i].name] + [ author_lastname.get_last_name_first(self.authors[i].name) ] + astats[i]
            for i in range(len(astats)) ]
        return (header, data)

    def get_authors_count_for_one_author(self, author_name, start_year, end_year, pub_type):
        astats = [0, 0, 0]
        for p in self.publications:
            if ( (start_year == None or p.year >= start_year) and
                (end_year == None or p.year <= end_year) and
                (pub_type == 4 or pub_type == p.pub_type) ):
                for a in p.authors:
                    if a == self.author_idx[author_name]:
                        astats[0] += author_count.appearing_first(a, p.authors)
                        astats[1] += author_count.appearing_last(a, p.authors)
                        astats[2] += author_count.appearing_sole(a, p.authors)
        return (astats)

    def search_authors(self, author):
        authors = []
        tmp_authors_1 = []
        tmp_authors_2 = []
        tmp_authors_3 = []
        tmp_authors_4 = []
        tmp_authors_5 = []
        tmp_authors_6 = []
        ordered_authors = []

        if author == "None" or author == "":
            return ordered_authors

        for a in self.authors:
            if author.lower() in a.name.lower():
                authors.append(a.name)

        splitted_author = author.split()

        if len(splitted_author) == 1:
            len_of_author = len(author)
            for a in authors:
                name_list = a.split()
                if  ((len(name_list[-1]) >= len_of_author) and (author.lower() == name_list[-1][:len_of_author].lower())):
                    tmp_authors_1.append(a)
                elif ((len(name_list[0]) >= len_of_author) and (author.lower() == name_list[0][:len_of_author].lower())):
                    tmp_authors_2.append(a)
                elif ((len(name_list) > 2) and (len(name_list[1]) >= len_of_author) and (author.lower() == name_list[1][:len_of_author].lower())):
                    tmp_authors_3.append(a)
                elif ((len(name_list) > 3) and (len(name_list[2]) >= len_of_author) and (author.lower() == name_list[2][:len_of_author].lower())):
                    tmp_authors_4.append(a)
                elif ((len(name_list) > 4) and (len(name_list[3]) >= len_of_author) and (author.lower() == name_list[3][:len_of_author].lower())):
                    tmp_authors_5.append(a)
                else:
                    tmp_authors_6.append(a)

            tmp_auth_1 = []
            tmp_auth_2 = []
            for a in tmp_authors_1:
                name_list = a.split()
                if(author.lower() == name_list[-1].lower()):
                    tmp_auth_1.append(a)
                else:
                    tmp_auth_2.append(a)
            tmp_authors_1 = sorted(tmp_auth_1, key=str.lower) + sorted(tmp_auth_2, key=lambda s: s.split()[-1])

            tmp_auth_1 = []
            tmp_auth_2 = []
            for a in tmp_authors_2:
                name_list = a.split()
                if(author.lower() == name_list[0].lower()):
                    tmp_auth_1.append(a)
                else:
                    tmp_auth_2.append(a)
            tmp_authors_2 = sorted(tmp_auth_1, key=lambda s: s.split()[-1]) + sorted(tmp_auth_2, key=str.lower)

            tmp_auth_1 = []
            tmp_auth_2 = []
            for a in tmp_authors_3:
                name_list = a.split()
                if(author.lower() == name_list[1].lower()):
                    tmp_auth_1.append(a)
                else:
                    tmp_auth_2.append(a)
            tmp_authors_3 = sorted(tmp_auth_1, key=lambda s: s.split()[-1]) + sorted(tmp_auth_2, key=lambda s: s.split()[1])

            tmp_auth_1 = []
            tmp_auth_2 = []
            for a in tmp_authors_4:
                name_list = a.split()
                if(author.lower() == name_list[2].lower()):
                    tmp_auth_1.append(a)
                else:
                    tmp_auth_2.append(a)
            tmp_authors_4 = sorted(tmp_auth_1, key=lambda s: s.split()[-1]) + sorted(tmp_auth_2, key=lambda s: s.split()[2])

            tmp_auth_1 = []
            tmp_auth_2 = []
            for a in tmp_authors_5:
                name_list = a.split()
                if(author.lower() == name_list[3].lower()):
                    tmp_auth_1.append(a)
                else:
                    tmp_auth_2.append(a)
            tmp_authors_5 = sorted(tmp_auth_1, key=lambda s: s.split()[-1]) + sorted(tmp_auth_2, key=lambda s: s.split()[3])

            tmp_authors_6 = sorted(tmp_authors_6, key=lambda s: s.split()[-1])

            ordered_authors = tmp_authors_1 + tmp_authors_2 + tmp_authors_3 + tmp_authors_4 + tmp_authors_5 + tmp_authors_6

        else:
            ordered_authors = sorted(authors, key=lambda s: s.split()[-1])

        return (ordered_authors)

    def get_author_stats(self,author):
        coauthors = {}
        papernumber = journalnumber = booknumber = booksnumber = allpubnumber = coauthornumber = first = last = 0
        author_name = ''
        author_found = False
        astats = [[0, 0, 0, 0, 0, 0, 0, 0] for _ in range(len(self.authors))]
        # The overall number of publications,papers,articls,book chapters,books
        # The number of co-authors
        # The number of times
        for p in self.publications:
            for a in p.authors:
                astats[a][p.pub_type + 1] += 1
                for a2 in p.authors:
                    if a != a2:
                        try:
                            coauthors[a].add(a2)
                        except KeyError:
                            coauthors[a] = set([a2])
                astats[a][5] = len(coauthors[a])
                astats[a][6] += author_count.appearing_first(a, p.authors)
                astats[a][7] += author_count.appearing_last(a, p.authors)
            for a in p.authors:
                astats[a][0] = astats[a][1] + astats[a][2] + astats[a][3] + astats[a][4]

        data = [ astats[i]
                for i in range(len(astats))]
        for i in range(len(data)):
            if author != "None" and author != "" and author.lower() in self.authors[i].name.lower():
                allpubnumber = data[i][0]
                papernumber = data[i][1]
                journalnumber = data[i][2]
                booknumber = data[i][3]
                booksnumber = data[i][4]
                coauthornumber = data[i][5]
                first = data[i][6]
                last = data[i][7]
                author_found = True
                author_name = self.authors[i].name
        return (author_found, allpubnumber, papernumber, journalnumber, booknumber, booksnumber,
                    coauthornumber, first, last, author_name)

    def get_author_stats_by_click(self,author):
        coauthors = {}
        author_name = ''
        author_found = False
        NoPublications = [0, 0, 0, 0, 0]
        NoFirstAuthor = [0, 0, 0, 0, 0]
        NoLastAuthor = [0, 0, 0, 0, 0]
        NoSoleAuthor = [0, 0, 0, 0, 0]
        NoCoAuthor = 0

        for p in self.publications:
            for a in p.authors:
                if str(self.authors[a].name) == author:
                    author_found = True
                    author_name = self.authors[a].name
                    NoPublications[p.pub_type + 1] += 1
                    for a2 in p.authors:
                        if a != a2:
                            try:
                                coauthors[a].add(a2)
                            except KeyError:
                                coauthors[a] = set([a2])
                    try:
                        NoCoAuthor = len(coauthors[a])
                    except:
                        NoCoAuthor = 0
                    NoFirstAuthor[p.pub_type + 1] += author_count.appearing_first(a, p.authors)
                    NoLastAuthor[p.pub_type + 1] += author_count.appearing_last(a, p.authors)
                    NoSoleAuthor[p.pub_type + 1] += author_count.appearing_sole(a, p.authors)

                    NoPublications[0] = NoPublications[1] + NoPublications[2] + NoPublications[3] + NoPublications[4]
                    NoFirstAuthor[0] = NoFirstAuthor[1] + NoFirstAuthor[2] + NoFirstAuthor[3] + NoFirstAuthor[4]
                    NoLastAuthor[0] = NoLastAuthor[1] + NoLastAuthor[2] + NoLastAuthor[3] + NoLastAuthor[4]
                    NoSoleAuthor[0] = NoSoleAuthor[1] + NoSoleAuthor[2] + NoSoleAuthor[3] + NoSoleAuthor[4]

        return (author_found, NoPublications, NoFirstAuthor, NoLastAuthor, NoSoleAuthor, NoCoAuthor, author_name)


    def get_average_authors_per_publication_by_year(self, av):
        header = ("Year", "Conference papers",
            "Journals", "Books",
            "Book chapers", "All publications")

        ystats = {}
        for p in self.publications:
            try:
                ystats[p.year][p.pub_type].append(len(p.authors))
            except KeyError:
                ystats[p.year] = [[], [], [], []]
                ystats[p.year][p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [ [y]
            + [ func(L) for L in ystats[y] ]
            + [ func(list(itertools.chain(*ystats[y]))) ]
            for y in ystats ]
        return (header, data)

    def get_publications_by_year(self):
        header = ("Year", "Number of conference papers",
            "Number of journals", "Number of books",
            "Number of book chapers", "Total")

        ystats = {}
        for p in self.publications:
            try:
                ystats[p.year][p.pub_type] += 1
            except KeyError:
                ystats[p.year] = [0, 0, 0, 0]
                ystats[p.year][p.pub_type] += 1

        data = [ [y] + ystats[y] + [sum(ystats[y])] for y in ystats ]
        return (header, data)

    def get_average_publications_per_author_by_year(self, av):
        header = ("Year", "Conference papers",
            "Journals", "Books",
            "Book chapers", "All publications")

        ystats = {}
        for p in self.publications:
            try:
                s = ystats[p.year]
            except KeyError:
                s = np.zeros((len(self.authors), 4))
                ystats[p.year] = s
            for a in p.authors:
                s[a][p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [ [y]
            + [ func(ystats[y][:, i]) for i in np.arange(4) ]
            + [ func(ystats[y].sum(axis=1)) ]
            for y in ystats ]
        return (header, data)

    def get_author_totals_by_year(self):
        header = ("Year", "No. of conference papers",
            "No. of journals", "No. of books",
            "No. of book chapers", "Total")

        ystats = {}
        for p in self.publications:
            try:
                s = ystats[p.year][p.pub_type]
            except KeyError:
                ystats[p.year] = [set(), set(), set(), set()]
                s = ystats[p.year][p.pub_type]
            for a in p.authors:
                s.add(a)
        data = [ [y] + [len(s) for s in ystats[y]] + [len(ystats[y][0] | ystats[y][1] | ystats[y][2] | ystats[y][3])]
            for y in ystats ]
        return (header, data)

    def add_publication(self, pub_type, title, year, authors):
        if year == None or len(authors) == 0:
            print ("Warning: excluding publication due to missing information")
            print ("    Publication type:", PublicationType[pub_type])
            print ("    Title:", title)
            print ("    Year:", year)
            print ("    Authors:", ",".join(authors))
            return
        if title == None:
            print ("Warning: adding publication with missing title [ %s %s (%s) ]" % (PublicationType[pub_type], year, ",".join(authors)))
        idlist = []
        for a in authors:
            try:
                idlist.append(self.author_idx[a])
            except KeyError:
                a_id = len(self.authors)
                self.author_idx[a] = a_id
                idlist.append(a_id)
                self.authors.append(Author(a))
        self.publications.append(
            Publication(pub_type, title, year, idlist))
        if (len(self.publications) % 100000) == 0:
            print ("Adding publication number %d (number of authors is %d)" % (len(self.publications), len(self.authors)))

        if self.min_year == None or year < self.min_year:
            self.min_year = year
        if self.max_year == None or year > self.max_year:
            self.max_year = year

    def _get_collaborations(self, author_id, include_self):
        data = {}
        for p in self.publications:
            if author_id in p.authors:
                for a in p.authors:
                    try:
                        data[a] += 1
                    except KeyError:
                        data[a] = 1
        if not include_self:
            del data[author_id]
        return data

    def get_coauthor_details(self, name):
        author_id = self.author_idx[name]
        data = self._get_collaborations(author_id, True)
        return [ (self.authors[key].name, data[key])
            for key in data ]

    def get_network_data(self):
        na = len(self.authors)

        nodes = [ [self.authors[i].name, -1] for i in range(na) ]
        links = set()
        for a in range(na):
            collab = self._get_collaborations(a, False)
            nodes[a][1] = len(collab)
            for a2 in collab:
                if a < a2:
                    links.add((a, a2))
        return (nodes, links)

    def get_degrees_of_separation(self, author1, author2):
        global checked_coauthors
        coauthors = {}
        separation_list = []
        checked_coauthors = {}
        for p in self.publications:
            for a in p.authors:
                for a2 in p.authors:
                    if a != a2:
                        try:
                            coauthors[self.authors[a].name].add(self.authors[a2].name)
                        except KeyError:
                            coauthors[self.authors[a].name] = set([self.authors[a2].name])
        try:
            list_of_coauthors_for_author1 = coauthors[author1]
        except:
            list_of_coauthors_for_author1 = []
        if author2 in list_of_coauthors_for_author1:
            return 0
        else:
            if len(list_of_coauthors_for_author1) == 0:
                return 'X'
            else:
                result = self.aux_func_deg_of_sep(author1, author2, coauthors, separation_list, -1)
                if (result == 100000):
                    return 'X'
                else:
                    return result               

    def aux_func_deg_of_sep(self, author1, author2, coauthors, separation_list, degree):
        global checked_coauthors
        degree += 1
        try:
            list_of_coauthors_for_author1 = coauthors[author1]
        except:
            list_of_coauthors_for_author1 = []
        for a in list_of_coauthors_for_author1:
            if a in checked_coauthors:
                pass
            else:
                checked_coauthors[a] = degree
        for a in list_of_coauthors_for_author1:
            if a in checked_coauthors:
                if checked_coauthors[a] >= degree:
                    if author2 == a:
                        sep_value = degree
                    else:
                        sep_value = self.aux_func_deg_of_sep(a, author2, coauthors, separation_list, degree)
                    separation_list.append(sep_value)
            else:
                if author2 == a:
                    sep_value = degree
                else:
                    sep_value = self.aux_func_deg_of_sep(a, author2, coauthors, separation_list, degree)
                separation_list.append(sep_value)
        if len(separation_list) == 0:
            return 100000
        else:
            return min(separation_list)
            
class DocumentHandler(handler.ContentHandler):
    TITLE_TAGS = [ "sub", "sup", "i", "tt", "ref" ]
    PUB_TYPE = {
        "inproceedings":Publication.CONFERENCE_PAPER,
        "article":Publication.JOURNAL,
        "book":Publication.BOOK,
        "incollection":Publication.BOOK_CHAPTER }

    def __init__(self, db):
        self.tag = None
        self.chrs = ""
        self.clearData()
        self.db = db

    def clearData(self):
        self.pub_type = None
        self.authors = []
        self.year = None
        self.title = None

    def startDocument(self):
        pass

    def endDocument(self):
        pass

    def startElement(self, name, attrs):
        if name in self.TITLE_TAGS:
            return
        if name in DocumentHandler.PUB_TYPE.keys():
            self.pub_type = DocumentHandler.PUB_TYPE[name]
        self.tag = name
        self.chrs = ""

    def endElement(self, name):
        if self.pub_type == None:
            return
        if name in self.TITLE_TAGS:
            return
        d = self.chrs.strip()
        if self.tag == "author":
            self.authors.append(d)
        elif self.tag == "title":
            self.title = d
        elif self.tag == "year":
            self.year = int(d)
        elif name in DocumentHandler.PUB_TYPE.keys():
            self.db.add_publication(
                self.pub_type,
                self.title,
                self.year,
                self.authors)
            self.clearData()
        self.tag = None
        self.chrs = ""

    def characters(self, chrs):
        if self.pub_type != None:
            self.chrs += chrs
