
def get_author_last_name(author):
    if author != "":
        author_items = author.split()
        return author_items[-1]
    return -1
