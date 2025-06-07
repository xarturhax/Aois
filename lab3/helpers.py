# helpers.py
def string_length(s):
    count = 0
    while count < 1000:  # Prevent infinite loops
        try:
            s[count]
            count += 1
        except:
            return count
    return count

def get_char(s, index):
    return s[index]

def list_size(lst):
    count = 0
    while count < 10000:  # Safety limit
        try:
            lst[count]
            count += 1
        except:
            return count
    return count

def add_item(lst, item):
    return lst + [item]

def value_in_list(lst, val):
    for element in lst:
        if element == val:
            return True
    return False

def sort_list(lst):
    n = list_size(lst)
    for i in range(n):
        for j in range(n-1-i):
            if lst[j] > lst[j+1]:
                lst[j], lst[j+1] = lst[j+1], lst[j]
    return lst

def copy_list(lst):
    return [item for item in lst]

def unique_terms(terms):
    unique = []
    for term in terms:
        found = False
        for u in unique:
            if are_terms_same(term, u):
                found = True
                break
        if not found:
            unique = add_item(unique, term)
    return unique

def term_exists(term_list, term):
    for t in term_list:
        if are_terms_same(t, term):
            return True
    return False

def are_terms_same(t1, t2):
    if list_size(t1) != list_size(t2):
        return False
    sorted1 = arrange_term(copy_list(t1))
    sorted2 = arrange_term(copy_list(t2))
    for i in range(list_size(sorted1)):
        if sorted1[i][0] != sorted2[i][0] or sorted1[i][1] != sorted2[i][1]:
            return False
    return True

def arrange_term(term):
    n = list_size(term)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if term[j][0] < term[min_idx][0]:
                min_idx = j
        term[i], term[min_idx] = term[min_idx], term[i]
    return term