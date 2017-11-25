
def get_author_last_name(author):
    if author != "":
        author_items = author.split()
        return author_items[-1]
    return -1

def get_last_name_first(author):
    if author != "":
        author_items = author.split()
        new_author_items = []
        first_names = ","
        if len(author_items) > 0:
            for item in author_items: #Check the author name does not contain extraneous characters (like numbers)
                if not item.isdigit():
                    new_author_items.append(item)
            if len(new_author_items) > 0:
                if len(new_author_items) > 1:
                    for item in new_author_items[:-1]:
                        first_names += " " + item.title() #Capitalise first letter
                    return new_author_items[-1].title() + first_names
                else:
                    return new_author_items[-1].title()
    return -1
