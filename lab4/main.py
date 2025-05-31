from prettytable import PrettyTable


def generate_truth_combinations(num_vars):
    """Генерирует все возможные комбинации значений истинности для заданного числа переменных"""
    return [[int(x) for x in f"{i:0{num_vars}b}"] for i in range(2 ** num_vars)]


def generate_canonical_forms(truth_data, var_names):
    """Генерирует совершенные нормальные формы (СДНФ и СКНФ) из таблицы истинности"""
    sdnf_terms, sknf_terms = [], []
    sdnf_nums, sknf_nums = [], []

    for idx, row in enumerate(truth_data):
        inputs, output = row[:-1], row[-1]
        sdnf_term = []
        sknf_clause = []

        for var, val in zip(var_names, inputs):
            if val:
                sdnf_term.append(var)
                sknf_clause.append(f"¬{var}")
            else:
                sdnf_term.append(f"¬{var}")
                sknf_clause.append(var)

        if output:
            sdnf_terms.append(f"({' ∧ '.join(sdnf_term)})")
            sdnf_nums.append(str(idx))
        else:
            sknf_terms.append(f"({' ∨ '.join(sknf_clause)})")
            sknf_nums.append(str(idx))

    return " ∨ ".join(sdnf_terms), " ∧ ".join(sknf_terms), sdnf_nums, sknf_nums


def find_prime_implicants(term_patterns):
    """Находит простые импликанты с использованием метода Квайна-МакКласки"""
    num_vars = len(term_patterns[0]) if term_patterns else 0
    current_implicants = [(p, {i}) for i, p in enumerate(term_patterns)]
    prime_list = []

    while current_implicants:
        new_implicants = []
        used = set()

        for i in range(len(current_implicants)):
            for j in range(i + 1, len(current_implicants)):
                p1, cov1 = current_implicants[i]
                p2, cov2 = current_implicants[j]
                diff_pos = [k for k in range(num_vars) if p1[k] != p2[k]]

                if len(diff_pos) == 1:
                    pos = diff_pos[0]
                    new_pat = p1[:pos] + '-' + p1[pos + 1:]
                    new_cov = cov1.union(cov2)
                    new_imp = (new_pat, new_cov)

                    if new_imp not in new_implicants:
                        new_implicants.append(new_imp)
                    used.add(i)
                    used.add(j)

        for idx, imp in enumerate(current_implicants):
            if idx not in used:
                prime_list.append(imp)

        current_implicants = new_implicants

    return prime_list


def count_literals(pattern):
    """Подсчитывает количество литералов в шаблоне"""
    return sum(1 for ch in pattern if ch != '-')


def find_optimal_cover(primes, all_terms):
    """Находит минимальное покрытие с использованием алгоритма ветвей и границ"""
    best_solution = None
    min_cost = float('inf')

    def backtrack(selection, covered, start_idx):
        nonlocal best_solution, min_cost
        if covered == all_terms:
            current_cost = sum(count_literals(primes[i][0]) for i in selection)
            if current_cost < min_cost:
                min_cost = current_cost
                best_solution = selection.copy()
            return

        for i in range(start_idx, len(primes)):
            new_covered = covered.union(primes[i][1])
            if new_covered != covered:
                selection.append(i)
                backtrack(selection, new_covered, i + 1)
                selection.pop()

    backtrack([], set(), 0)
    return [primes[i] for i in best_solution] if best_solution else []


def minimize_expression(canonical_form, var_names):
    """Минимизирует логическое выражение"""
    if not canonical_form:
        return ""

    term_patterns = []
    for term in canonical_form.split(' ∨ '):
        pattern = []
        term = term.strip('()')
        for var in var_names:
            if f"¬{var}" in term:
                pattern.append('0')
            elif var in term:
                pattern.append('1')
            else:
                pattern.append('-')
        term_patterns.append(''.join(pattern))

    primes = find_prime_implicants(term_patterns)
    all_terms = set(range(len(term_patterns)))
    solution = find_optimal_cover(primes, all_terms)

    def pattern_to_term(pattern):
        literals = []
        for i, ch in enumerate(pattern):
            if ch == '1':
                literals.append(var_names[i])
            elif ch == '0':
                literals.append(f"¬{var_names[i]}")
        return f"({' ∧ '.join(literals)})" if literals else "1"

    return " ∨ ".join(pattern_to_term(imp[0]) for imp in solution)


def create_karnaugh_map(var_count, values):
    """Создает карту Карно для заданного числа переменных"""
    if var_count == 2:
        return [[values[0], values[1]],
                [values[2], values[3]]]
    elif var_count == 3:
        return [[values[0], values[1], values[3], values[2]],
                [values[4], values[5], values[7], values[6]]]
    elif var_count == 4:
        return [[values[0], values[1], values[3], values[2]],
                [values[4], values[5], values[7], values[6]],
                [values[12], values[13], values[15], values[14]],
                [values[8], values[9], values[11], values[10]]]
    return None


def display_karnaugh_map(kmap, variables):
    """Отображает карту Карно в удобном формате"""
    var_count = len(variables)
    print("\n" + "═" * 50)
    print("Карта Карно:".center(50))
    print("═" * 50)

    if var_count == 2:
        table = PrettyTable()
        table.field_names = [f"{variables[1]}=0", f"{variables[1]}=1"]
        table.add_row([kmap[0][0], kmap[0][1]], divider=True)
        table.add_row([kmap[1][0], kmap[1][1]])
        print(f"{variables[0]}=0")
        print(f"{variables[0]}=1")
        print(table)
    elif var_count == 3:
        table = PrettyTable()
        table.field_names = ["", "00", "01", "11", "10"]
        table.add_row([f"{variables[0]}=0"] + kmap[0], divider=True)
        table.add_row([f"{variables[0]}=1"] + kmap[1])
        print(table)
    elif var_count == 4:
        table = PrettyTable()
        table.field_names = ["", "00", "01", "11", "10"]
        table.add_row(["00"] + kmap[0], divider=True)
        table.add_row(["01"] + kmap[1], divider=True)
        table.add_row(["11"] + kmap[2], divider=True)
        table.add_row(["10"] + kmap[3])
        print(table)


class BinaryAdder3Bit:
    """Класс для реализации 3-битного сумматора"""

    def __init__(self):
        self.sum_logic = lambda a, b, c: a ^ b ^ c
        self.carry_logic = lambda a, b, c: (a & b) | (a & c) | (b & c)

    def add_bits(self, a, b, carry_in=0):
        """Складывает три бита и возвращает сумму и перенос"""
        sum_bit = self.sum_logic(a, b, carry_in)
        carry_out = self.carry_logic(a, b, carry_in)
        return sum_bit, carry_out

    def add_numbers(self, num1, num2):
        """Складывает два 4-битных числа"""
        if not 0 <= num1 <= 15 or not 0 <= num2 <= 15:
            raise ValueError("Числа должны быть в диапазоне 0-15")

        bits1 = [int(b) for b in f"{num1:04b}"]
        bits2 = [int(b) for b in f"{num2:04b}"]
        result = []
        carry = 0

        for i in range(3, -1, -1):
            s, carry = self.add_bits(bits1[i], bits2[i], carry)
            result.insert(0, s)

        result.insert(0, carry)
        return result


class D8421Converter:
    """Класс для преобразования кода D8421 в D8421+1"""

    def __init__(self):
        self.output_logic = [
            lambda d8, d4, d2, d1: d8 ^ (d4 & d2 & d1),
            lambda d8, d4, d2, d1: d4 ^ (d2 & d1),
            lambda d8, d4, d2, d1: d2 ^ d1,
            lambda d8, d4, d2, d1: not d1
        ]

    def convert_code(self, decimal):
        """Преобразует десятичное число в код D8421+1"""
        if not 0 <= decimal <= 9:
            raise ValueError("Число должно быть от 0 до 9")

        input_bits = [int(b) for b in f"{decimal:04b}"]
        output_bits = [
            int(self.output_logic[0](*input_bits)),
            int(self.output_logic[1](*input_bits)),
            int(self.output_logic[2](*input_bits)),
            int(self.output_logic[3](*input_bits))
        ]

        output_decimal = output_bits[0] * 8 + output_bits[1] * 4 + output_bits[2] * 2 + output_bits[3] * 1

        return {
            'input': {'decimal': decimal, 'binary': input_bits},
            'output': {'binary': output_bits, 'decimal': output_decimal if output_decimal < 10 else None}
        }


def analyze_3bit_adder():
    """Анализирует работу 3-битного сумматора"""
    print("\n" + "═" * 80)
    print(" АНАЛИЗ 3-БИТНОГО СУММАТОРА ".center(80))
    print("═" * 80)

    # Таблица истинности для сумматора
    truth_data = [
        [0, 0, 0, 0, 0], [0, 0, 1, 1, 0],
        [0, 1, 0, 1, 0], [0, 1, 1, 0, 1],
        [1, 0, 0, 1, 0], [1, 0, 1, 0, 1],
        [1, 1, 0, 0, 1], [1, 1, 1, 1, 1]
    ]
    vars = ['A', 'B', 'Cin']

    # Создаем красивую таблицу для вывода
    truth_table = PrettyTable()
    truth_table.field_names = ["A", "B", "Cin", "S", "Cout"]
    truth_table.align = "c"
    for row in truth_data:
        truth_table.add_row(row)

    print("\n" + "─" * 50)
    print("ТАБЛИЦА ИСТИННОСТИ".center(50))
    print("─" * 50)
    print(truth_table)

    # Анализ выхода S (сумма)
    s_data = [row[:3] + [row[3]] for row in truth_data]
    s_values = [row[3] for row in truth_data]

    print("\n" + "─" * 50)
    print("АНАЛИЗ ВЫХОДА S (СУММА)".center(50))
    print("─" * 50)

    sdnf, sknf, sdnf_nums, sknf_nums = generate_canonical_forms(s_data, vars)
    print("\nСДНФ:", sdnf)
    print("Индексы:", ", ".join(sdnf_nums))
    minimized = minimize_expression(sdnf, vars)
    print("Минимизированная форма:", minimized)

    kmap = create_karnaugh_map(3, s_values)
    display_karnaugh_map(kmap, vars)

    # Анализ выхода Cout (перенос)
    cout_data = [row[:3] + [row[4]] for row in truth_data]
    cout_values = [row[4] for row in truth_data]

    print("\n" + "─" * 50)
    print("АНАЛИЗ ВЫХОДА Cout (ПЕРЕНОС)".center(50))
    print("─" * 50)

    sdnf, sknf, sdnf_nums, sknf_nums = generate_canonical_forms(cout_data, vars)
    print("\nСДНФ:", sdnf)
    print("Индексы:", ", ".join(sdnf_nums))
    minimized = minimize_expression(sdnf, vars)
    print("Минимизированная форма:", minimized)

    kmap = create_karnaugh_map(3, cout_values)
    display_karnaugh_map(kmap, vars)

    # Демонстрация работы
    print("\n" + "═" * 50)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ СУММАТОРА".center(50))
    print("═" * 50)

    adder = BinaryAdder3Bit()
    num1, num2 = 6, 9

    print(f"\nСложение чисел {num1} и {num2}:")

    # Таблица для вывода чисел
    num_table = PrettyTable()
    num_table.field_names = ["Число", "Двоичное представление"]
    num_table.add_row([num1, f"{num1:04b}"])
    num_table.add_row([num2, f"{num2:04b}"])
    print(num_table)

    result = adder.add_numbers(num1, num2)
    decimal = result[0] * 16 + result[1] * 8 + result[2] * 4 + result[3] * 2 + result[4] * 1

    # Таблица для вывода результата
    result_table = PrettyTable()
    result_table.field_names = ["Перенос", "Биты суммы", "Десятичное значение"]
    result_table.add_row([result[0], result[1:], decimal])
    print("\nРезультат:")
    print(result_table)


def analyze_code_converter():
    """Анализирует преобразователь кода D8421 в D8421+1"""
    print("\n" + "═" * 80)
    print(" АНАЛИЗ ПРЕОБРАЗОВАТЕЛЯ D8421 → D8421+1 ".center(80))
    print("═" * 80)

    # Таблица истинности
    truth_data = [
        [0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 0, 1, 1], [0, 0, 1, 1, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 1], [0, 1, 0, 1, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 1, 1, 1], [0, 1, 1, 1, 1, 0, 0, 0],
        [1, 0, 0, 0, 1, 0, 0, 1], [1, 0, 0, 1, 1, 0, 1, 0],
        [1, 0, 1, 0, None, None, None, None], [1, 0, 1, 1, None, None, None, None],
        [1, 1, 0, 0, None, None, None, None], [1, 1, 0, 1, None, None, None, None],
        [1, 1, 1, 0, None, None, None, None], [1, 1, 1, 1, None, None, None, None]
    ]
    input_vars = ['D8', 'D4', 'D2', 'D1']
    output_vars = ['Y3', 'Y2', 'Y1', 'Y0']

    # Создаем красивую таблицу для вывода
    truth_table = PrettyTable()
    truth_table.field_names = ["D8", "D4", "D2", "D1", "Y3", "Y2", "Y1", "Y0"]
    truth_table.align = "c"
    for row in truth_data:
        truth_table.add_row([row[0], row[1], row[2], row[3],
                             'X' if row[4] is None else row[4],
                             'X' if row[5] is None else row[5],
                             'X' if row[6] is None else row[6],
                             'X' if row[7] is None else row[7]])

    print("\n" + "─" * 80)
    print("ТАБЛИЦА ИСТИННОСТИ".center(80))
    print("─" * 80)
    print(truth_table)

    # Анализ для каждого выхода
    for out_idx, out_var in enumerate(output_vars, 4):
        print("\n" + "─" * 50)
        print(f"АНАЛИЗ ВЫХОДА {out_var}".center(50))
        print("─" * 50)

        valid_data = [row[:4] + [row[out_idx]] for row in truth_data if row[out_idx] is not None]
        sdnf, _, sdnf_nums, _ = generate_canonical_forms(valid_data, input_vars)

        print("\nСДНФ:", sdnf)
        print("Индексы:", ", ".join(sdnf_nums))
        minimized = minimize_expression(sdnf, input_vars)
        print("Минимизированная форма:", minimized)

        values = [row[out_idx] if row[out_idx] is not None else None for row in truth_data]
        kmap = create_karnaugh_map(4, values)
        display_karnaugh_map(kmap, input_vars)

    # Демонстрация работы
    print("\n" + "═" * 50)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ ПРЕОБРАЗОВАТЕЛЯ".center(50))
    print("═" * 50)

    converter = D8421Converter()

    while True:
        try:
            value = input("\nВведите число от 0 до 9 (или 'q' для выхода): ")
            if value.lower() == 'q':
                break

            num = int(value)
            if not 0 <= num <= 9:
                print("Число должно быть от 0 до 9!")
                continue

            result = converter.convert_code(num)

            # Таблица для вывода результата преобразования
            result_table = PrettyTable()
            result_table.field_names = ["Параметр", "Значение"]
            result_table.add_row(["Входное число", result['input']['decimal']])
            result_table.add_row(["Входной код (D8421)", ' '.join(map(str, result['input']['binary']))])
            result_table.add_row(["Выходной код (D8421+1)", ' '.join(map(str, result['output']['binary']))])
            result_table.add_row(
                ["Выходное число", result['output']['decimal'] if result['output']['decimal'] is not None else "N/A"])

            print("\nРезультат преобразования:")
            print(result_table)

        except ValueError:
            print("Ошибка: введите целое число от 0 до 9!")


if __name__ == "__main__":
    analyze_3bit_adder()
    analyze_code_converter()
