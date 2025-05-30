import re
from typing import List

def check_formula_validity(formula: str) -> bool:
    """Проверяет, содержит ли формула только допустимые символы."""
    pattern = r'^[a-zA-Z|&!~>\-() ]+$'
    return bool(re.match(pattern, formula))

def construct_cnf(table: List[List[int]], vars: List[str]) -> str:
    """Строит конъюнктивную нормальную форму (КНФ) из таблицы истинности."""
    clauses = [
        f"({'|'.join([f'{'!' if row[j] else ''}{vars[j]}' for j in range(len(vars))])})"
        for row in table if row[-1] == 0
    ]
    return '&'.join(clauses) if clauses else ''

def construct_dnf(table: List[List[int]], vars: List[str]) -> str:
    """Строит дизъюнктивную нормальную форму (ДНФ) из таблицы истинности."""
    clauses = [
        f"({'&'.join([f'{'!' if not row[j] else ''}{vars[j]}' for j in range(len(vars))])})"
        for row in table if row[-1] == 1
    ]
    return '|'.join(clauses) if clauses else ''

def cnf_binary_form(table: List[List[int]], vars: List[str]) -> str:
    """Генерирует бинарное представление КНФ."""
    terms = [''.join(map(str, row[:-1])) for row in table if row[-1] == 0]
    return f"&({','.join(terms)})" if terms else "&()"

def cnf_decimal_form(table: List[List[int]], vars: List[str]) -> str:
    """Генерирует десятичное представление КНФ."""
    terms = [convert_to_decimal(''.join(map(str, row[:-1]))) for row in table if row[-1] == 0]
    return f"&({','.join(terms)})" if terms else "&()"

def dnf_binary_form(table: List[List[int]], vars: List[str]) -> str:
    """Генерирует бинарное представление ДНФ."""
    terms = [''.join(map(str, row[:-1])) for row in table if row[-1] == 1]
    return f"|({','.join(terms)})" if terms else "|()"

def dnf_decimal_form(table: List[List[int]], vars: List[str]) -> str:
    """Генерирует десятичное представление ДНФ."""
    terms = [convert_to_decimal(''.join(map(str, row[:-1]))) for row in table if row[-1] == 1]
    return f"|({','.join(terms)})" if terms else "|()"

def get_binary_index(table: List[List[int]]) -> str:
    """Генерирует бинарный индекс из результатов таблицы истинности."""
    return ''.join(str(row[-1]) for row in table)

def convert_to_decimal(binary: str) -> str:
    """Преобразует бинарную строку в десятичное число."""
    return str(int(binary, 2)) if binary else '0'
