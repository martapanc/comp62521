def appearing_first(name, author_list):
    if name == author_list[0]:
        return 1
    return 0

def appearing_last(name, author_list):
    tmp_len = len(author_list)
    if name == author_list[-1]:
        return 1
    return 0
