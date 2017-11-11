def appearing_first(name, author_list):
    t = 0
    if name == author_list[0]:
        t = 1
    return t

def appearing_last(name, author_list):
    t = 0
    tmp_len = len(author_list)
    if name == author_list[tmp_len - 1]:
        t = 1
    return t
