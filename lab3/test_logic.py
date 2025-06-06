import pytest
from boolean_expression import generate_truth_table, eval_expr, validate_input, print_truth_table, replace_implication_equivalence, is_balanced
from normal_forms import NormalFormGenerator, Minimizer


# --- Тесты для boolean_expression.py ---



@pytest.mark.parametrize("expr, expected", [
    ("a|b&c", [0,0,0,1,1,1,1,1]),
    ("a>(b~c)", [1,1,1,1,1,0,0,1]),
    ("!a>(!b~!c)", [1,0,0,1,1,1,1,1]),
])
def test_generate_truth_table(expr, expected):
    table = generate_truth_table(expr)
    results = [row['result'] for row in table]
    assert results == expected

@pytest.mark.parametrize("expr", [
    "a#b", "a&&b", "a|", ""
])
def test_generate_truth_table_invalid(expr):
    with pytest.raises(ValueError):
        generate_truth_table(expr)

# Тесты для eval_expr
@pytest.mark.parametrize("expr, expected", [
    ("0|0", 0),
    ("0|1", 1),
    ("1|0", 1),
    ("1|1", 1),
    ("0&0", 0),
    ("0&1", 0),
    ("1&0", 0),
    ("1&1", 1),
    ("!0", 1),
    ("!1", 0),
    ("0>0", 1),
    ("0>1", 1),
    ("1>0", 0),
    ("1>1", 1),
    ("0~0", 1),
    ("0~1", 0),
    ("1~0", 0),
    ("1~1", 1),
    ("(0|0)", 0),
    ("(0|1)", 1),
    ("(1|0)", 1),
    ("(1|1)", 1),
    ("(0&0)", 0),
    ("(0&1)", 0),
    ("(1&0)", 0),
    ("(1&1)", 1),
    ("(!0)", 1),
    ("(!1)", 0),
    ("(0>0)", 1),
    ("(0>1)", 1),
    ("(1>0)", 0),
    ("(1>1)", 1),
    ("(0~0)", 1),
    ("(0~1)", 0),
    ("(1~0)", 0),
    ("(1~1)", 1),
])
def test_eval_expr(expr, expected):
    assert eval_expr(expr) == expected

# Тесты для validate_input
@pytest.mark.parametrize("expr, expected", [
    ("a|b", True),
    ("a&b", True),
    ("a>b", True),
    ("a~b", True),
    ("!a", True),
    ("a#b", False),
    ("a&&b", False),
    ("a|", False),
    ("", False),
    ("(a|b)", True),
    ("(a&b)", True),
    ("(a>b)", True),
    ("(a~b)", True),
    ("(!a)", True),
    ("(a#b)", False),
    ("(a&&b)", False),
    ("(a|)", False),
    ("()", False),
])
def test_validate_input(expr, expected):
    assert validate_input(expr) == expected

# Тесты для print_truth_table
def test_print_truth_table(capsys):
    table = generate_truth_table("a|b")
    print_truth_table(table)
    out = capsys.readouterr().out
    assert "a | b | F" in out
    assert "0 | 0 | 0" in out
    assert "0 | 1 | 1" in out
    assert "1 | 0 | 1" in out
    assert "1 | 1 | 1" in out


# --- Тесты для normal_forms.py ---

def test_normal_form_generator():
    table = generate_truth_table("a|b&c")
    gen = NormalFormGenerator(table)
    assert gen.generate_sdnf() == "(!a&b&c)|(a&!b&!c)|(a&!b&c)|(a&b&!c)|(a&b&c)"
    assert gen.generate_sknf() == "(a|b|c)&(a|b|!c)&(a|!b|c)"

def test_minimizer_dnf_cnf():
    table = generate_truth_table("a|b&c")
    minz = Minimizer(table)
    mdnf = minz.calculation_method()
    mcnf = minz.calculation_method(cnf=True)
    assert "(b&c)" in mdnf and "(a&!b)" in mdnf and "(a&!c)" in mdnf
    assert "(a|b)" in mcnf and "(a|c)" in mcnf

def test_minimizer_tabular_methods():
    table = generate_truth_table("a|b&c")
    minz = Minimizer(table)
    mdnf = minz.calculation_tabular_method()
    mcnf = minz.calculation_tabular_method(cnf=True)
    assert "(b&c)" in mdnf and "(a&!b)" in mdnf and "(a&!c)" in mdnf
    assert "(a|b)" in mcnf and "(a|c)" in mcnf

# --- Интеграционный тест для main.py ---

import pytest
from main import process_expression


def test_process_expression_complex(capsys):
    # Тест со сложным выражением
    process_expression("a>(b~c)")
    out = capsys.readouterr().out
    assert "Таблица истинности" in out
    assert "СДНФ" in out
    assert "СКНФ" in out
    assert "Минимизированная ДНФ" in out

def test_process_expression_with_not(capsys):
    # Тест с отрицанием
    process_expression("!a|!b")
    out = capsys.readouterr().out
    assert "Таблица истинности" in out
    assert "СДНФ" in out
    assert "СКНФ" in out
    assert "Минимизированная ДНФ" in out

def test_process_expression_with_parentheses(capsys):
    # Тест с вложенными скобками
    process_expression("(a|b)&(b|c)")
    out = capsys.readouterr().out
    assert "Таблица истинности" in out
    assert "СДНФ" in out
    assert "СКНФ" in out
    assert "Минимизированная ДНФ" in out

def test_process_expression_invalid_operator(capsys):
    # Тест с недопустимым оператором
    process_expression("a#b")
    out = capsys.readouterr().out
    assert "Ошибка" in out

def test_process_expression_invalid_syntax(capsys):
    # Тест с недопустимым синтаксисом
    process_expression("a&&b")
    out = capsys.readouterr().out
    assert "Ошибка" in out


def test_process_expression_single_variable(capsys):
    # Тест с одной переменной
    process_expression("a")
    out = capsys.readouterr().out
    assert "Таблица истинности" in out
    assert "СДНФ" in out
    assert "СКНФ" in out
    assert "Минимизированная ДНФ" in out

def test_process_expression_single_not(capsys):
    # Тест с одним отрицанием
    process_expression("!a")
    out = capsys.readouterr().out
    assert "Таблица истинности" in out
    assert "СДНФ" in out
    assert "СКНФ" in out
    assert "Минимизированная ДНФ" in out

def test_process_expression_complex_nested(capsys):
    # Тест со сложным вложенным выражением
    process_expression("!((a|b)&(b|c))")
    out = capsys.readouterr().out
    assert "Таблица истинности" in out
    assert "СДНФ" in out
    assert "СКНФ" in out
    assert "Минимизированная ДНФ" in out

def test_process_expression_all_operators(capsys):
    # Тест со всеми операторами
    process_expression("a|b&c>!a~b")
    out = capsys.readouterr().out
    assert "Таблица истинности" in out
    assert "СДНФ" in out
    assert "СКНФ" in out
    assert "Минимизированная ДНФ" in out

def test_process_expression_invalid_variable(capsys):
    # Тест с недопустимой переменной
    process_expression("a|d")
    out = capsys.readouterr().out
    assert "Ошибка" in out

def test_process_expression_valid(capsys):
    process_expression("a|b&c")
    out = capsys.readouterr().out
    assert "Таблица истинности" in out
    assert "СДНФ" in out
    assert "СКНФ" in out
    assert "Минимизированная ДНФ" in out

def test_process_expression_invalid(capsys):
    process_expression("a#b")
    out = capsys.readouterr().out
    assert "Ошибка" in out

def test_process_expression_empty(capsys):
    process_expression("")
    out = capsys.readouterr().out
    assert "Ошибка" in out

# Тесты для replace_implication_equivalence
@pytest.mark.parametrize("expr, expected", [
    ("a>b", "(not a) or b"),
    ("a~b", "((a) and (b)) or (not (a) and not (b))"),
    ("(a>b)", "((not a) or b)"),
    ("(a~b)", "(((a) and (b)) or (not (a) and not (b)))"),
])
def test_replace_implication_equivalence(expr, expected):
    result = replace_implication_equivalence(expr)
    assert result == expected

@pytest.mark.parametrize("expr, expected", [
    ("a>b>c", "(not a) or (not b) or c"),
    ("a>b~c", "(((not a) or b) and (c)) or (not ((not a) or b) and not (c))"),
])
def test_replace_implication_equivalence_complex(expr, expected):
    result = replace_implication_equivalence(expr)
    assert result == expected

@pytest.mark.parametrize("expr", [
    "a~b~c",  # Двойная эквиваленция
])
def test_replace_implication_equivalence_invalid(expr):
    with pytest.raises(ValueError):
        replace_implication_equivalence(expr)

# Тесты для is_balanced
@pytest.mark.parametrize("expr, expected", [
    ("(a|b)", True),
    ("((a|b))", True),
    ("(a|(b&c))", True),
    ("(a|b", False),
    ("a|b)", False),
    ("((a|b)", False),
    ("(a|b))", False),
    ("", True),
    ("a", True),
])
def test_is_balanced(expr, expected):
    assert is_balanced(expr) == expected

# Дополнительные тесты для validate_input
@pytest.mark.parametrize("expr, expected", [
    ("a|b|c", True),
    ("a&b&c", True),
    ("a>b>c", True),
    ("a~b~c", True),
    ("!a|!b|!c", True),
    ("(a|b)&(b|c)", True),
    ("!((a|b)&(b|c))", True),
    ("a b", False),  # Пробел
    ("a#b", False),  # Недопустимый символ
    ("a&&b", False),  # Двойной оператор
    ("a|", False),   # Оператор в конце
    ("a|b|", False), # Оператор в конце
    ("a|b|c|", False), # Оператор в конце
    ("a|b|c|d", False), # Недопустимая переменная
    ("a|b|c|1", False), # Недопустимый символ
    ("a|b|c|!", False), # Оператор в конце
    ("!a|b|c", True),  # Отрицание в начале
    ("a|!b|c", True),  # Отрицание в середине
    ("a|b|!c", True),  # Отрицание в конце
    ("!a|!b|!c", True), # Несколько отрицаний
    ("!(a|b)", True),   # Отрицание скобок
    ("!((a|b)&(b|c))", True), # Сложное отрицание
])
def test_validate_input_complex(expr, expected):
    assert validate_input(expr) == expected

# Тесты для print_truth_table
def test_print_truth_table_empty(capsys):
    print_truth_table([])
    out = capsys.readouterr().out
    assert out == ""

def test_print_truth_table_single_var(capsys):
    table = [{'a': 0, 'result': 0}, {'a': 1, 'result': 1}]
    print_truth_table(table)
    out = capsys.readouterr().out
    assert "a | F" in out
    assert "0 | 0" in out
    assert "1 | 1" in out

def test_print_truth_table_two_vars(capsys):
    table = [
        {'a': 0, 'b': 0, 'result': 0},
        {'a': 0, 'b': 1, 'result': 1},
        {'a': 1, 'b': 0, 'result': 1},
        {'a': 1, 'b': 1, 'result': 1}
    ]
    print_truth_table(table)
    out = capsys.readouterr().out
    assert "a | b | F" in out
    assert "0 | 0 | 0" in out
    assert "0 | 1 | 1" in out
    assert "1 | 0 | 1" in out
    assert "1 | 1 | 1" in out

def test_print_truth_table_three_vars(capsys):
    table = [
        {'a': 0, 'b': 0, 'c': 0, 'result': 0},
        {'a': 0, 'b': 0, 'c': 1, 'result': 1},
        {'a': 0, 'b': 1, 'c': 0, 'result': 1},
        {'a': 0, 'b': 1, 'c': 1, 'result': 1},
        {'a': 1, 'b': 0, 'c': 0, 'result': 1},
        {'a': 1, 'b': 0, 'c': 1, 'result': 1},
        {'a': 1, 'b': 1, 'c': 0, 'result': 1},
        {'a': 1, 'b': 1, 'c': 1, 'result': 1}
    ]
    print_truth_table(table)
    out = capsys.readouterr().out
    assert "a | b | c | F" in out
    assert "0 | 0 | 0 | 0" in out
    assert "0 | 0 | 1 | 1" in out
    assert "0 | 1 | 0 | 1" in out
    assert "0 | 1 | 1 | 1" in out
    assert "1 | 0 | 0 | 1" in out
    assert "1 | 0 | 1 | 1" in out
    assert "1 | 1 | 0 | 1" in out
    assert "1 | 1 | 1 | 1" in out 