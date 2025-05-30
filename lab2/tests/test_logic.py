import pytest
from src.formula_utils import *
from src.logic_table import *
from src.main import present_results


# Tests for formula_utils.py
def test_check_formula_validity():
    assert check_formula_validity("a & b") == True
    assert check_formula_validity("a + b") == False  # Invalid symbol
    assert check_formula_validity("") == False
    assert check_formula_validity("!a | b") == True


def test_construct_cnf():
    table = [[0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
    vars = ['a', 'b']
    assert construct_cnf(table, vars) == ''  # Always true
    table = [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 0]]
    assert construct_cnf(table, vars) == '(a|b)&(a|!b)&(!a|b)&(!a|!b)'


def test_construct_dnf():
    table = [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 0]]
    vars = ['a', 'b']
    assert construct_dnf(table, vars) == ''  # Always false
    table = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
    assert construct_dnf(table, vars) == '(!a&b)|(a&!b)|(a&b)'  # Corrected expected output


def test_cnf_binary_form():
    table = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
    vars = ['a', 'b']
    assert cnf_binary_form(table, vars) == '&(00)'  # Corrected expected output


def test_cnf_decimal_form():
    table = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
    vars = ['a', 'b']
    assert cnf_decimal_form(table, vars) == '&(0)'  # Corrected expected output


def test_dnf_binary_form():
    table = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
    vars = ['a', 'b']
    assert dnf_binary_form(table, vars) == '|(01,10,11)'  # Corrected expected output


def test_dnf_decimal_form():
    table = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
    vars = ['a', 'b']
    assert dnf_decimal_form(table, vars) == '|(1,2,3)'  # Corrected expected output


def test_get_binary_index():
    table = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
    assert get_binary_index(table) == '0111'


def test_convert_to_decimal():
    assert convert_to_decimal("0111") == "7"
    assert convert_to_decimal("1111") == "15"
    assert convert_to_decimal("") == "0"


# Tests for logic_table.py
def test_infix_to_postfix():
    assert infix_to_postfix("a & b") == "ab&"
    assert infix_to_postfix("a | b") == "ab|"
    assert infix_to_postfix("!a") == "a!"
    assert infix_to_postfix("(a & b) | c") == "ab&c|"
    assert infix_to_postfix("a & !b") == "ab!&"


def test_compute_postfix():
    assert compute_postfix([0, 0], "ab&", ['a', 'b']) == 0
    assert compute_postfix([1, 0], "ab|", ['a', 'b']) == 1
    assert compute_postfix([1], "a!", ['a']) == 0
    assert compute_postfix([1, 0], "ab&", ['a', 'b']) == 0
    assert compute_postfix([1, 1], "ab|", ['a', 'b']) == 1


def test_create_truth_table():
    table, vars = create_truth_table("a & b", show=False)
    assert vars == ['a', 'b']
    assert table == [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1]]
    table, vars = create_truth_table("!a", show=False)
    assert vars == ['a']
    assert table == [[0, 1], [1, 0]]


def test_display_header(capsys):
    display_header(['a', 'b'])
    captured = capsys.readouterr()
    assert "a | b | Результат" in captured.out
    display_header(['x'])
    captured = capsys.readouterr()
    assert "x | Результат" in captured.out


# Tests for main.py
def test_present_results(capsys):
    with pytest.raises(ValueError, match="Формула содержит недопустимые символы!"):
        present_results("a + b")

    present_results("a & b")
    captured = capsys.readouterr()
    assert "КНФ" in captured.out
    assert "ДНФ" in captured.out
    assert "КНФ (бинарная)" in captured.out  # Corrected expected label
    assert "ДНФ (десятичная)" in captured.out
