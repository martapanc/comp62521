
def get_author_last_name(author):
    if author != "":
        author_items = author.split()
        return author_items[-1]
    return -1

def get_last_name_first(author):
    if author != "":
        author_items = author.split()
        first_names = ","
        for item in author_items: #Check the author name does not contain extraneous characters (like numbers)
            if item.isdigit():
                author_items.remove(item)
        if len(author_items) > 1:
            for item in author_items[:-1]:
                first_names += " " + item.title() #Capitalise first letter
            return author_items[-1].title() + first_names
        else:
            return author_items[-1].title()
    return -1
