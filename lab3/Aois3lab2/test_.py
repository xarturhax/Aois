import pytest
from tablica import true_table, reversed_polish_notation
from snf import create_sdnf, create_sknf, check_input, gluing, print_dnf, print_knf, print_mdnf, print_mknf
from raschet import calculation_method
from raschet_tablich import calculation_tabular_method
from karno import table_method
from main import main
from io import StringIO
from unittest.mock import patch

# Тесты для tablica.py
@pytest.mark.parametrize("formula, expected_rpn", [
    ("a|b", "ab|"),
    ("a&b", "ab&"),
    ("a>b", "ab>"),
    ("a~b", "ab~"),
    ("a|b&c", "abc&|"),
    ("(a|b)&c", "ab|c&"),
    ("!(!a|!b)|c", "a!b!|!c|"),
])
def test_reversed_polish_notation(formula, expected_rpn):
    assert reversed_polish_notation(formula) == expected_rpn

@pytest.mark.parametrize("formula, vars_count, expected_results", [
    ("a|b", 2, [0, 1, 1, 1]),
    ("a&b", 2, [0, 0, 0, 1]),
    ("a|b&c", 3, [0, 0, 0, 1, 1, 1, 1, 1]),
    ("!(!a|!b)|c", 3, [0, 1, 0, 1, 0, 1, 1, 1]),
])
def test_true_table(formula, vars_count, expected_results):
    table, vars = true_table(formula)
    assert len(vars) == vars_count
    assert len(table) == 2 ** vars_count
    assert [table[i][-1] for i in range(len(table))] == expected_results

# Добавлен тест для обработки ошибок в true_table
def test_true_table_invalid_input():
    with pytest.raises(ValueError, match="Invalid RPN"):
        true_table("a&&b")

# Тесты для snf.py
def test_create_sdnf_two_vars():
    table, vars = true_table("a|b")
    sdnf = create_sdnf(table, vars)
    assert sdnf == "(!a&b)|(a&!b)|(a&b)"

def test_create_sdnf_three_vars():
    table, vars = true_table("a|b&c")
    sdnf = create_sdnf(table, vars)
    assert sdnf == "(!a&b&c)|(a&!b&!c)|(a&!b&c)|(a&b&!c)|(a&b&c)"

def test_create_sknf_two_vars():
    table, vars = true_table("a&b")
    sknf = create_sknf(table, vars)
    assert "&".join(sorted(sknf.split("&"))) == "&".join(sorted("(a|b)&(!a|b)&(a|!b)".split("&")))

def test_create_sknf_three_vars():
    table, vars = true_table("a|b&c")
    sknf = create_sknf(table, vars)
    assert sknf == "(a|b|c)&(a|b|!c)&(a|!b|c)"

def test_check_input():
    assert check_input("a|b") == True
    assert check_input("(a&b)|c") == True
    assert check_input("123") == False
    assert check_input("") == False
    assert check_input("a#b") == False

def test_gluing():
    snf = [["!a", "b"], ["a", "b"]]
    result = gluing(snf)
    assert result == [["b"]]

def test_print_dnf(capsys):
    dnf = [["a"], ["b"]]
    print_dnf(dnf)
    captured = capsys.readouterr()
    assert captured.out == "ДНФ: (a)|(b)\n"

def test_print_knf(capsys):
    knf = [["a", "b"]]
    print_knf(knf)
    captured = capsys.readouterr()
    assert captured.out == "КНФ: (a|b)\n"

def test_print_mdnf(capsys):
    mdnf = [["a"], ["b"]]
    print_mdnf(mdnf)
    captured = capsys.readouterr()
    assert captured.out == "Минимизированная ДНФ: (a)|(b)\n"

def test_print_mknf(capsys):
    mknf = [["a", "b"]]
    print_mknf(mknf)
    captured = capsys.readouterr()
    assert captured.out == "Минимизированная КНФ: (a|b)\n"

# Тесты для raschet.py
@pytest.mark.parametrize("sdnf, expected_mdnf", [
    ([["!a", "b"], ["a", "!b"], ["a", "b"]], [["a"], ["b"]]),
    ([["a", "b", "c"], ["a", "!b", "c"], ["!a", "b", "c"]], [["a", "c"], ["b", "c"]]),
    ([["a"]], [["a"]]),
])
def test_calculation_method_dnf(sdnf, expected_mdnf):
    mdnf = calculation_method(sdnf, is_dnf=True)
    assert sorted(mdnf) == sorted(expected_mdnf)

@pytest.mark.parametrize("sknf, expected_mknf", [
    ([["a", "b"], ["!a", "b"], ["a", "!b"]], [["b"], ["a"]]),
    ([["a", "b", "c"], ["a", "!b", "c"], ["a", "b", "!c"]], [["a", "b"], ["a", "c"]]),
    ([["!a"]], [["!a"]]),
])
def test_calculation_method_cnf(sknf, expected_mknf):
    mknf = calculation_method(sknf, is_dnf=False)
    assert sorted(mknf) == sorted(expected_mknf)

# Тесты для raschet_tablich.py
def test_calculation_tabular_method_dnf_two_vars():
    prime_implicants = [["a"], ["b"]]
    subsumed_implicants = [["!a", "b"], ["a", "!b"], ["a", "b"]]
    mdnf = calculation_tabular_method(prime_implicants, subsumed_implicants)
    assert sorted(mdnf) == sorted([["a"], ["b"]])

def test_calculation_tabular_method_empty_subsumed():
    prime_implicants = [["a"]]
    subsumed_implicants = []
    mdnf = calculation_tabular_method(prime_implicants, subsumed_implicants)
    assert mdnf == [["a"]]

# Тесты для karno.py
@pytest.mark.parametrize("table, vars_count, mdnf, mknf, expected_result_parts", [
    ([0, 1, 1, 1], 2, [["a"], ["b"]], [["a", "b"]], ["MDNF: (a2)", "MCNF: "]),
    ([0, 0, 0, 1, 1, 1, 1, 1], 3, [["a"], ["b", "c"]], [["a", "b"], ["a", "c"]], ["MDNF: (a2&a3)|(a1&!a2)", "MCNF: (a1|a2)"]),
])
def test_table_method(table, vars_count, mdnf, mknf, expected_result_parts):
    result = table_method(table, mdnf, mknf, vars_count)
    for part in expected_result_parts:
        assert part in result

# Интеграционные тесты для main.py
def test_main_a_or_b(capsys):
    with patch('builtins.input', return_value="a|b"):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()
            assert "СДНФ: (!a&b)|(a&!b)|(a&b)" in output
            assert "СКНФ: (a|b)" in output
            assert "Минимизированная ДНФ: (a)|(b)" in output or "Минимизированная ДНФ: (b)|(a)" in output
            assert "Минимизированная КНФ: (a|b)" in output

def test_main_invalid_input():
    with patch('builtins.input', return_value="a#b"):
        with pytest.raises(Exception, match="Некорректный ввод!"):
            main()