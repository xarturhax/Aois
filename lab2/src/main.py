from src.formula_utils import *
from src.logic_table import *

def present_results(formula: str) -> None:
    """Выводит различные формы логической формулы."""
    if not check_formula_validity(formula):
        raise ValueError("Формула содержит недопустимые символы!")
    table, variables = create_truth_table(formula)
    def show_section(label: str, content: str) -> None:
        print(f"{'-' * 40}\n{label}: {content}")
    show_section("КНФ", construct_cnf(table, variables))
    show_section("ДНФ", construct_dnf(table, variables))
    show_section("КНФ (бинарная)", cnf_binary_form(table, variables))
    show_section("КНФ (десятичная)", cnf_decimal_form(table, variables))
    show_section("ДНФ (бинарная)", dnf_binary_form(table, variables))
    show_section("ДНФ (десятичная)", dnf_decimal_form(table, variables))
    show_section("Бинарный индекс", get_binary_index(table))
    show_section("Десятичный индекс", convert_to_decimal(get_binary_index(table)))

def execute():
    """Основная функция для запуска программы."""
    formula = input("Введите логическую формулу: ")
    present_results(formula)

if __name__ == "__main__":
    execute()
