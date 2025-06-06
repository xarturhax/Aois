from boolean_expression import generate_truth_table
from normal_forms import NormalFormGenerator, Minimizer

def validate_input(formula: str) -> bool:
    if not formula:
        return False
    stack = []
    for char in formula:
        if char == '(': stack.append(char)
        elif char == ')':
            if not stack: return False
            stack.pop()
    if stack: return False
    valid_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!&|>()~')
    return all(c in valid_chars for c in formula)

def print_truth_table(truth_table):
    if not truth_table:
        print("Нет данных для таблицы истинности.")
        return
    variables = [v for v in truth_table[0] if v != 'result']
    print(' | '.join(variables) + ' | F')
    print('-' * (4 * len(variables) + 3))
    for row in truth_table:
        print(' | '.join(str(row[v]) for v in variables) + f" | {row['result']}")

def process_expression(expression: str) -> None:
    try:
        if not validate_input(expression):
            print("Ошибка: Неверный синтаксис выражения. Используйте только переменные (a, b, c), операторы (!, &, |, >, ~) и скобки.")
            return
        truth_table = generate_truth_table(expression)
        if not truth_table:
            print("Ошибка: Не удалось сгенерировать таблицу истинности")
            return
        generator = NormalFormGenerator(truth_table)
        dnf = generator.generate_dnf()
        cnf = generator.generate_cnf()
        print("\nТаблица истинности:")
        print_truth_table(truth_table)
        print(f"\nСДНФ: {dnf if dnf else 'нет'}")
        print(f"СКНФ: {cnf if cnf else 'нет'}")
        minimizer = Minimizer(truth_table)
        print("\nМинимизация методом расчета:")
        print(f"Минимизированная ДНФ: {minimizer.calculation_method() or 'нет'}")
        print(f"Минимизированная КНФ: {minimizer.calculation_method(cnf=True) or 'нет'}")
        print("\nРасчётно-табличный метод:")
        print(f"Минимизированная ДНФ: {minimizer.calculation_tabular_method() or 'нет'}")
        print(f"Минимизированная КНФ: {minimizer.calculation_tabular_method(cnf=True) or 'нет'}")
        print("\nТабличный метод (карно):")
        print(f"Минимизированная ДНФ: {minimizer.table_method() or 'нет'}")
    except ValueError as e:
        print(f"Ошибка: {str(e)}")
    except Exception as e:
        print(f"Неожиданная ошибка: {str(e)}")

def main():
    while True:
        expr = input("\nВведите формулу (или 'q' для выхода):\n").strip()
        if expr.lower() == 'q':
            break
        if not expr:
            continue
        print(f"Введена формула: {expr}")
        process_expression(expr)

if __name__ == "__main__":
    main()
