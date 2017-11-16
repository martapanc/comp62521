
def get_author_last_name(author):
    if author != "":
        author_items = author.split()
        return author_items[-1]
    return -1

def get_last_name_first(author):
    author_items = author.split()
    first_names = ","
    if len(author_items) > 1:
        for item in author_items[:-1]:
            first_names += " " + item
        return author_items[-1] + first_names
    else:
        return author_items[-1]
