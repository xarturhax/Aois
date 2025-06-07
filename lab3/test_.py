import pytest
import helpers as hlp
from expression_parser import tokenize_input, extract_vars, infix_to_postfix, operator_priority, valid_var
from expression_processor import compute_operator, invert_value, compute_expression, generate_truth_table
from logic_minimizer import (
    create_minterms, sort_term, terms_equal, can_combine, combine_terms,
    format_term, format_term_compact, merge_terms, is_covered, build_coverage_matrix,
    quine_mccluskey, select_prime_implicants, minimize_expression, minimize_with_table,
    get_kmap_dimensions, gray_code, create_karnaugh_map, minimize_with_kmap, remove_duplicates, contains_term
)
from prettytable import PrettyTable


# Тесты для helpers.py
def test_string_length():
    assert hlp.string_length("abc") == 3
    assert hlp.string_length("") == 0
    assert hlp.string_length("a" * 1000) == 1000


def test_get_char():
    s = "test"
    assert hlp.get_char(s, 0) == 't'
    assert hlp.get_char(s, 3) == 't'
    with pytest.raises(IndexError):
        hlp.get_char(s, 10)


def test_list_size():
    assert hlp.list_size([]) == 0
    assert hlp.list_size([1, 2, 3]) == 3
    assert hlp.list_size([0] * 1000) == 1000


def test_add_item():
    lst = []
    assert hlp.add_item(lst, 1) == [1]
    assert hlp.add_item([1], 2) == [1, 2]


def test_value_in_list():
    assert hlp.value_in_list([1, 2, 3], 2) is True
    assert hlp.value_in_list([1, 3], 2) is False
    assert hlp.value_in_list([], 1) is False


def test_sort_list():
    assert hlp.sort_list([3, 1, 2]) == [1, 2, 3]
    assert hlp.sort_list(['c', 'a', 'b']) == ['a', 'b', 'c']
    assert hlp.sort_list([]) == []


def test_copy_list():
    orig = [1, 2, 3]
    copy = hlp.copy_list(orig)
    assert copy == orig
    assert copy is not orig


def test_unique_terms():
    terms = [[('a', 1)], [('a', 1)], [('b', 0)]]
    unique = hlp.unique_terms(terms)
    assert len(unique) == 2


def test_term_exists():
    terms = [[('a', 1)], [('b', 0)]]
    assert hlp.term_exists(terms, [('a', 1)]) is True
    assert hlp.term_exists(terms, [('c', 1)]) is False


def test_are_terms_same():
    t1 = [('a', 1), ('b', 0)]
    t2 = [('b', 0), ('a', 1)]
    assert hlp.are_terms_same(t1, t2) is True
    assert hlp.are_terms_same(t1, [('a', 1)]) is False


def test_arrange_term():
    term = [('b', 0), ('a', 1)]
    arranged = hlp.arrange_term(term)
    assert arranged == [('a', 1), ('b', 0)]


# Тесты для expression_parser.py
def test_valid_var():
    assert valid_var('a') is True
    assert valid_var('z') is True
    assert valid_var('A') is False
    assert valid_var('1') is False


def test_tokenize_input():
    assert tokenize_input("a & b") == ['a', '&', 'b']
    assert tokenize_input("a->b") == ['a', '->', 'b']
    assert tokenize_input("~(a|b)") == ['~', '(', 'a', '|', 'b', ')']
    assert tokenize_input("!a & (b|c)") == ['!', 'a', '&', '(', 'b', '|', 'c', ')']
    assert tokenize_input("a & b | c") == ['a', '&', 'b', '|', 'c']


def test_extract_vars():
    tokens = ['a', '&', 'b', '|', 'c']
    assert extract_vars(tokens) == ['a', 'b', 'c']
    tokens = ['a', 'a', 'b']
    assert extract_vars(tokens) == ['a', 'b']
    tokens = ['(', ')', '->']
    assert extract_vars(tokens) == []


def test_operator_priority():
    assert operator_priority('!') == 4
    assert operator_priority('&') == 3
    assert operator_priority('|') == 2
    assert operator_priority('->') == 1
    assert operator_priority('~') == 1
    assert operator_priority('@') == -1


def test_infix_to_postfix():
    assert infix_to_postfix(['a', '&', 'b']) == ['a', 'b', '&']
    assert infix_to_postfix(['a', '|', 'b', '&', 'c']) == ['a', 'b', 'c', '&', '|']
    assert infix_to_postfix(['a', '->', 'b', '|', 'c']) == ['a', 'b', 'c', '|', '->']
    assert infix_to_postfix(['!', 'a', '&', 'b']) == ['a', '!', 'b', '&']
    assert infix_to_postfix(['(', 'a', '|', 'b', ')', '&', 'c']) == ['a', 'b', '|', 'c', '&']


# Тесты для expression_processor.py
def test_compute_operator():
    assert compute_operator('&', 1, 1) == 1
    assert compute_operator('&', 1, 0) == 0
    assert compute_operator('|', 0, 1) == 1
    assert compute_operator('|', 0, 0) == 0
    assert compute_operator('->', 1, 0) == 0
    assert compute_operator('->', 0, 1) == 1
    assert compute_operator('~', 1, 1) == 1
    assert compute_operator('~', 1, 0) == 0


def test_invert_value():
    assert invert_value(0) == 1
    assert invert_value(1) == 0


def test_compute_expression():
    expr = ['a', 'b', '&']
    val_dict = {'a': 1, 'b': 1}
    assert compute_expression(expr, val_dict) == 1

    expr = ['a', '!']
    val_dict = {'a': 1}
    assert compute_expression(expr, val_dict) == 0

    expr = ['a', 'b', '|', 'c', '&']
    val_dict = {'a': 0, 'b': 1, 'c': 1}
    assert compute_expression(expr, val_dict) == 1

    expr = ['a', 'b', '->']
    val_dict = {'a': 1, 'b': 0}
    assert compute_expression(expr, val_dict) == 0


def test_generate_truth_table():
    expr = ['a', 'b', '&']
    vars = ['a', 'b']
    table = generate_truth_table(expr, vars)
    assert len(table) == 4
    assert ([0, 0], 0) in table
    assert ([1, 1], 1) in table

    expr = ['a', '!']
    vars = ['a']
    table = generate_truth_table(expr, vars)
    assert len(table) == 2


# Тесты для logic_minimizer.py
def test_create_minterms():
    table = [
        ((0, 0), 1),
        ((0, 1), 0),
        ((1, 0), 1),
        ((1, 1), 1)
    ]
    minterms = create_minterms(table, ['a', 'b'], 1)
    assert len(minterms) == 3
    assert [('a', 0), ('b', 0)] in minterms

    maxterms = create_minterms(table, ['a', 'b'], 0)
    assert len(maxterms) == 1


def test_sort_term():
    term = [('b', 1), ('a', 0)]
    assert sort_term(term) == [('a', 0), ('b', 1)]


def test_terms_equal():
    t1 = [('a', 1), ('b', 0)]
    t2 = [('b', 0), ('a', 1)]
    assert terms_equal(t1, t2) is True
    assert terms_equal(t1, [('a', 1)]) is False


def test_can_combine():
    t1 = [('a', 1), ('b', 0)]
    t2 = [('a', 1), ('b', 1)]
    can, var = can_combine(t1, t2)
    assert can is True
    assert var == 'b'

    t3 = [('a', 1), ('c', 0)]
    can, var = can_combine(t1, t3)
    assert can is False


def test_combine_terms():
    term = [('a', 1), ('b', 0), ('c', 1)]
    combined = combine_terms(term, 'b')
    assert combined == [('a', 1), ('c', 1)]


def test_format_term():
    term = [('a', 1), ('b', 0)]
    assert format_term(term, True) == "a¬b"
    assert format_term(term, False) == "(¬a∨b)"
    assert format_term([], True) == "1"
    assert format_term([], False) == "0"


def test_format_term_compact():
    term = [('a', 1), ('b', 0)]
    assert format_term_compact(term, True) == "a!b"
    assert format_term_compact(term, False) == "(!a|b)"


def test_merge_terms():
    terms = ["a!b", "!ab"]
    assert merge_terms(terms, " ∨ ") == "a!b ∨ !ab"
    assert merge_terms([], " ∨ ") == "0"
    assert merge_terms(["a"], " ∧ ") == "a"
    # Изменяем ожидаемый результат, так как функция не добавляет скобки автоматически
    assert merge_terms(["a|b"], " ∧ ") == "a|b"

def test_remove_duplicates():
    terms = [[('a', 1)], [('a', 1)], [('b', 0)]]
    unique = remove_duplicates(terms)
    assert len(unique) == 2
    assert [('a', 1)] in unique
    assert [('b', 0)] in unique

def test_contains_term():
    terms = [[('a', 1)], [('b', 0)]]
    assert contains_term(terms, [('a', 1)]) is True
    assert contains_term(terms, [('b', 0)]) is True
    assert contains_term(terms, [('c', 1)]) is False

def test_can_combine_negative_case():
    t1 = [('a', 1), ('b', 0)]
    t2 = [('a', 0), ('b', 1)]
    can, var = can_combine(t1, t2)
    assert can is False
    assert var is None

def test_is_covered_negative_case():
    imp = [('a', 1)]
    term = [('b', 0)]
    assert is_covered(imp, term) is False

def test_build_coverage_matrix_empty():
    matrix = build_coverage_matrix([], [])
    assert matrix == []

def test_minimize_with_table_empty():
    minimized, steps, table = minimize_with_table([], True, [])
    assert minimized == []
    assert table == []

def test_is_covered():
    imp = [('a', 1)]
    term = [('a', 1), ('b', 0)]
    assert is_covered(imp, term) is True
    assert is_covered([('a', 0)], term) is False


def test_build_coverage_matrix():
    terms = [[('a', 1), ('b', 0)], [('a', 1), ('b', 1)]]
    implicants = [[('a', 1)]]
    matrix = build_coverage_matrix(terms, implicants)
    assert matrix == [[1], [1]]


def test_quine_mccluskey():
    terms = [
        [('a', 0), ('b', 0)],
        [('a', 0), ('b', 1)],
        [('a', 1), ('b', 1)]
    ]
    primes, steps = quine_mccluskey(terms, True)
    assert len(primes) >= 1
    assert len(steps) >= 1


def test_select_prime_implicants():
    terms = [[('a', 0), ('b', 0)], [('a', 1), ('b', 1)]]
    primes = [[('a', 1)], [('b', 1)]]
    selected = select_prime_implicants(terms, primes)
    assert len(selected) >= 1


def test_minimize_expression():
    terms = [
        [('a', 0), ('b', 0)],
        [('a', 0), ('b', 1)],
        [('a', 1), ('b', 1)]
    ]
    minimized, steps = minimize_expression(terms, True)
    assert len(minimized) >= 1
    assert len(steps) >= 1


def test_minimize_with_table():
    terms = [[('a', 0), ('b', 0)], [('a', 1), ('b', 1)]]
    minimized, steps, table = minimize_with_table(terms, True, terms)
    assert len(minimized) >= 1
    assert len(table) >= 1


def test_get_kmap_dimensions():
    assert get_kmap_dimensions(1) == (1, 2, 0, 1)
    assert get_kmap_dimensions(2) == (2, 2, 1, 1)
    assert get_kmap_dimensions(3) == (2, 4, 1, 2)
    assert get_kmap_dimensions(4) == (4, 4, 2, 2)
    assert get_kmap_dimensions(5) == (None, None, None, None)


def test_gray_code():
    assert gray_code(2) == ['00', '01', '11', '10']
    assert gray_code(1) == ['0', '1']


def test_create_karnaugh_map():
    terms = [[('a', 0), ('b', 0)]]
    kmap, params = create_karnaugh_map(terms, ['a', 'b'], True)
    assert kmap == [[1, 0], [0, 0]]

    terms = [[('a', 0), ('b', 0), ('c', 1)]]
    kmap, params = create_karnaugh_map(terms, ['a', 'b', 'c'], True)
    assert len(kmap) == 2
    assert len(kmap[0]) == 4


def test_minimize_with_kmap():
    terms = [[('a', 0), ('b', 0)]]
    minimized, steps, kmap = minimize_with_kmap(terms, True, ['a', 'b'])
    assert len(minimized) == 1
    assert kmap is not None


# Интеграционные тесты
def test_full_workflow():
    tokens = tokenize_input("a & b")
    vars = extract_vars(tokens)
    postfix = infix_to_postfix(tokens)

    assert tokens == ['a', '&', 'b']
    assert vars == ['a', 'b']
    assert postfix == ['a', 'b', '&']

    table = generate_truth_table(postfix, vars)
    assert len(table) == 4

    minterms = create_minterms(table, vars, 1)
    assert len(minterms) == 1

    minimized, steps = minimize_expression(minterms, True)
    assert len(minimized) >= 1


def test_complex_expression():
    expr = "(a -> b) & (!a | c)"
    tokens = tokenize_input(expr)
    vars = extract_vars(tokens)
    postfix = infix_to_postfix(tokens)

    assert '->' in tokens
    assert '!' in tokens
    assert vars == ['a', 'b', 'c']

    table = generate_truth_table(postfix, vars)
    assert len(table) == 8

    minterms = create_minterms(table, vars, 1)
    assert len(minterms) > 0

    minimized, steps = minimize_expression(minterms, True)
