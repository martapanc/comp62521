from comp62521 import app
from comp62521.database import database
from flask import (render_template, request)
import json

def format_data(data):
    fmt = "%.2f"
    result = []
    for item in data:
        if type(item) is list:
            result.append(", ".join([ (fmt % i).rstrip('0').rstrip('.') for i in item ]))
        else:
            result.append((fmt % item).rstrip('0').rstrip('.'))
    return result

@app.route("/averages")
def showAverages():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":"averages"}
    args['title'] = "Averaged Data"
    tables = []
    headers = ["Average", "Conference Paper", "Journal", "Book", "Book Chapter", "All Publications"]
    averages = [ database.Stat.MEAN, database.Stat.MEDIAN, database.Stat.MODE ]
    tables.append({
        "id":1,
        "title":"Average Authors per Publication",
        "header":headers,
        "rows":[
                [ database.Stat.STR[i] ]
                + format_data(db.get_average_authors_per_publication(i)[1])
                for i in averages ] })
    tables.append({
        "id":2,
        "title":"Average Publications per Author",
        "header":headers,
        "rows":[
                [ database.Stat.STR[i] ]
                + format_data(db.get_average_publications_per_author(i)[1])
                for i in averages ] })
    tables.append({
        "id":3,
        "title":"Average Publications in a Year",
        "header":headers,
        "rows":[
                [ database.Stat.STR[i] ]
                + format_data(db.get_average_publications_in_a_year(i)[1])
                for i in averages ] })
    tables.append({
        "id":4,
        "title":"Average Authors in a Year",
        "header":headers,
        "rows":[
                [ database.Stat.STR[i] ]
                + format_data(db.get_average_authors_in_a_year(i)[1])
                for i in averages ] })

    args['tables'] = tables
    return render_template("averages.html", args=args)

@app.route("/coauthors")
def showCoAuthors():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    PUB_TYPES = ["Conference Papers", "Journals", "Books", "Book Chapters", "All Publications"]
    args = {"dataset":dataset, "id":"coauthors"}
    args["title"] = "Co-Authors"

    start_year = db.min_year
    if "start_year" in request.args:
        start_year = int(request.args.get("start_year"))

    end_year = db.max_year
    if "end_year" in request.args:
        end_year = int(request.args.get("end_year"))

    pub_type = 4
    if "pub_type" in request.args:
        pub_type = int(request.args.get("pub_type"))

    args["data"] = db.get_coauthor_data(start_year, end_year, pub_type)
    args["start_year"] = start_year
    args["end_year"] = end_year
    args["pub_type"] = pub_type
    args["min_year"] = db.min_year
    args["max_year"] = db.max_year
    args["start_year"] = start_year
    args["end_year"] = end_year
    args["pub_str"] = PUB_TYPES[pub_type]
    return render_template("coauthors.html", args=args)

@app.route("/")
def showStatisticsMenu():
    dataset = app.config['DATASET']
    args = {"dataset":dataset}
    return render_template('statistics.html', args=args)

@app.route("/statisticsdetails/<status>")
def showPublicationSummary(status):
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":status}

    if (status == "publication_summary"):
        args["title"] = "Publication Summary"
        args["data"] = db.get_publication_summary()

    if (status == "publication_author"):
        args["title"] = "Publications by Author"
        args["data"] = db.get_publications_by_author()
        args["status"] = status
        return render_template('publications_by_author.html', args=args)

    if (status == "publication_year"):
        args["title"] = "Publication by Year"
        args["data"] = db.get_publications_by_year()

    if (status == "author_year"):
        args["title"] = "Author by Year"
        args["data"] = db.get_author_totals_by_year()

    if (status == "all_details_of_authors"):
        args["title"] = "All the Details of the Authors"
        args["data"] = db.get_all_details_of_authors()

    return render_template('statistics_details.html', args=args)

@app.route("/authorcount")
def showAuthorsCount():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":"authors_count"}
    PUB_TYPES = ["Conference Papers", "Journals", "Books", "Book Chapters", "All Publications"]

    start_year = db.min_year
    if "start_year" in request.args:
        start_year = int(request.args.get("start_year"))

    end_year = db.max_year
    if "end_year" in request.args:
        end_year = int(request.args.get("end_year"))

    pub_type = 4
    if "pub_type" in request.args:
        pub_type = int(request.args.get("pub_type"))

    args["title"] = "Authors Count"
    args["data"] = db.get_authors_count(start_year, end_year, pub_type)
    args["pub_type"] = pub_type
    args["min_year"] = db.min_year
    args["max_year"] = db.max_year
    args["start_year"] = start_year
    args["end_year"] = end_year
    args["pub_str"] = PUB_TYPES[pub_type]

    return render_template('authors_count.html', args=args)

@app.route("/authorstats")
def showAuthorStats():
    dataset=app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":"author_stats"}
    args["title"] = "Author Stats"
    author = str(request.args.get("author"))
    author_found, allpubnumber, papernumber, journalnumber, booknumber, booksnumber, coauthornumber, first, last, author_name = db.get_author_stats(author)
    args["authorfound"]=author_found
    args["author"]=author
    args["allpubnumber"] = allpubnumber
    args["papernumber"] = papernumber
    args["journalnumber"] = journalnumber
    args["booknumber"] = booknumber
    args["booksnumber"] = booksnumber
    args["coauthornumber"] = coauthornumber
    args["first"] = first
    args["last"] = last
    args["authorname"] = author_name
    return render_template("author_stats.html", args=args)

@app.route("/authorsearch")
def showAuthorSearch():
    dataset=app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":"search_authors"}
    args["title"] = "Author Search"
    author = str(request.args.get("author"))
    authors = db.search_authors(author)
    args["authors"] = authors
    return render_template("author_search.html", args=args)


@app.route("/authorstatsbyclick")
def showAuthorSearchByClick():
    dataset=app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":"author_stats_by_click"}
    args["title"] = "Author Stats"
    author = str(request.args.get("author"))
    author_found, NoPublications, NoFirstAuthor, NoLastAuthor, NoSoleAuthor, NoCoAuthor, author_name = db.get_author_stats_by_click(author)
    args["authorfound"]=author_found
    args["author"]=author
    args["NoPublications"] = NoPublications
    args["NoFirstAuthor"] = NoFirstAuthor
    args["NoLastAuthor"] = NoLastAuthor
    args["NoSoleAuthor"] = NoSoleAuthor
    args["NoCoAuthor"] = NoCoAuthor
    args["authorname"] = author_name
    return render_template("author_stats_by_click.html", args=args)

@app.route("/degrees_of_separation")
def showDegreeOfSeparation():
    dataset=app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":"author_stats"}
    args["title"] = "Degrees of Separation"
    #author1 = str(request.args.get("author1"))
    #author2 = str(request.args.get("author2"))
    #degree = db.get_degrees_of_separation(author1,author2)
    #args["author1"] = author1
    #args["author2"] = author2
    #args["degree"] = degree
    return render_template("degrees_of_separation.html", args=args)

@app.route("/two_authors_nw_ajax")
def getTwoAuthorsNetwork():
    db = app.config['DATABASE']
    author1 = str(request.args.get("author1"))
    author2 = str(request.args.get("author2"))
    authors, coauthors = db.get_two_authors_network(author1, author2)
    degree = db.get_degrees_of_separation(author1, author2)
    data = {'author1': author1, 'author2': author2, 'authors': authors, 'coauthors': coauthors, 'degree': degree}
    return json.dumps(data)

@app.route("/single_author_network")
def showSingleAuthorNetwork():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset": dataset, "id": "single_author_network"}
    args["title"] = "Single author's Network"
    return render_template("single_author_network.html", args=args)

@app.route("/single_author_nw_ajax")
def showSingleAuthorNetworkAjax():
    db = app.config['DATABASE']
    author = str(request.args.get("author"))
    authors, coauthors = db.get_single_author_network(author)
    data = {'author_name': author, 'authors': authors, 'coauthors': coauthors}
    return json.dumps(data)

@app.route("/author_list")
def getAuthorList():
    db = app.config['DATABASE']
    author_list = db.get_authors_as_list()
    data = {'author_list': author_list}
    return json.dumps(data)