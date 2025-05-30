from prettytable import PrettyTable
import itertools
from raschet import *
from snf import *
from copy import deepcopy


class karno_map:
    def __init__(self, res, values):
        self.res = res
        self.value = values
        self.in_square = False
        self.is_in_4_square = False
        if self.res == 1:
            self.type = "dnf"
        else:
            self.type = "cnf"


def append_value(element):
    element.in_square = True


def table_method(value_table, mdnf, mknf, num_vars):
    table, table_of_values = PrettyTable(), []
    rows, cols = get_kmap_dimensions(num_vars)
    row_vars, col_vars = num_vars // 2, num_vars - num_vars // 2
    row_combinations = list(itertools.product([0, 1], repeat=row_vars))
    col_combinations = list(itertools.product([0, 1], repeat=col_vars))

    # Adjust order for Gray code-like arrangement
    row_combinations = reorder_gray_code(row_combinations)
    col_combinations = reorder_gray_code(col_combinations)

    table.field_names = [""] + [str(col) for col in col_combinations]
    for i, row in enumerate(row_combinations):
        row_data = [str(row)]
        for j, col in enumerate(col_combinations):
            index = get_table_index(row, col, row_vars, col_vars, len(value_table))
            row_data.append(value_table[index])
        table.add_row(row_data)

    print(table)
    print_mdnf(mdnf)
    print_mknf(mknf)

    for i in range(len(value_table)):
        values = list(itertools.product([0, 1], repeat=num_vars))[i]
        karno_map_element = karno_map(int(value_table[i]), list(values))
        table_of_values.append(karno_map_element)

    return making_squares(table_of_values, num_vars)


def get_kmap_dimensions(num_vars):
    if num_vars == 2:
        return 2, 2
    elif num_vars == 3:
        return 2, 4
    elif num_vars == 4:
        return 4, 4
    else:
        return 2, 2  # Default to 2 variables


def reorder_gray_code(combinations):
    result = [combinations[0]]
    for i in range(1, len(combinations)):
        prev = result[-1]
        for comb in combinations:
            if comb not in result and sum(a != b for a, b in zip(prev, comb)) == 1:
                result.append(comb)
                break
    return result


def get_table_index(row, col, row_vars, col_vars, table_size):
    binary = list(row) + list(col)
    index = 0
    for i, bit in enumerate(binary[::-1]):
        index += bit * (2 ** i)
    return min(index, table_size - 1)


def check_values(x, table, num_vars):
    square = [table[x].value]
    rows, cols = get_kmap_dimensions(num_vars)
    row, col = x // cols, x % cols
    neighbors = []

    # Check right neighbor (with wrap-around for 3 or 4 variables)
    right_col = (col + 1) % cols if num_vars >= 3 else col + 1
    if right_col < cols and not table[row * cols + right_col].in_square and table[row * cols + right_col].res == table[x].res:
        neighbors.append(row * cols + right_col)

    # Check bottom neighbor (with wrap-around for 4 variables)
    bottom_row = (row + 1) % rows if num_vars == 4 else row + 1
    if bottom_row < rows and not table[bottom_row * cols + col].in_square and table[bottom_row * cols + col].res == table[x].res:
        neighbors.append(bottom_row * cols + col)

    if not neighbors:
        return None, table

    for neighbor in neighbors:
        square.append(table[neighbor].value)
        table[neighbor].in_square = True

    return [deepcopy(square)], table


def making_squares(res_value_table, num_vars):
    array_of_squares_SDNF, array_of_squares_SCNF = [], []
    rows, cols = get_kmap_dimensions(num_vars)

    for x in range(len(res_value_table)):
        if res_value_table[x].in_square or res_value_table[x].is_in_4_square:
            continue
        square, res_value_table = check_values(x, res_value_table, num_vars)
        if square is not None:
            if res_value_table[x].type == "dnf":
                array_of_squares_SDNF.extend(square)
            else:
                array_of_squares_SCNF.extend(square)

        # Check for larger squares (2x2)
        big_square, res_value_table = checking_big_squares(x, res_value_table, num_vars)
        if big_square is not None:
            if res_value_table[x].type == "dnf":
                array_of_squares_SDNF.extend(big_square)
            else:
                array_of_squares_SCNF.extend(big_square)

    sdnf_res = minimizing_by_squares(array_of_squares_SDNF, 'sdnf', num_vars)
    scnf_res = minimizing_by_squares(array_of_squares_SCNF, 'scnf', num_vars)
    return f"MDNF: {sdnf_res}\nMCNF: {scnf_res}"


def checking_big_squares(x, table, num_vars):
    rows, cols = get_kmap_dimensions(num_vars)
    row, col = x // cols, x % cols
    indices = []

    # Check 2x2 square
    if row + 1 < rows and col + 1 < cols:
        indices = [x, x + 1, x + cols, x + cols + 1]
        if all(table[i].res == table[x].res and not table[i].in_square and not table[i].is_in_4_square for i in indices):
            square = [table[i].value for i in indices]
            for i in indices:
                table[i].is_in_4_square = True
            return [deepcopy(square)], table

    # Check wrap-around for 3 variables (e.g., columns 0 and 3)
    if num_vars == 3 and col == 0:
        indices = [x, x + 3, x + cols, x + cols + 3]
        if all(table[i].res == table[x].res and not table[i].in_square and not table[i].is_in_4_square for i in indices):
            square = [table[i].value for i in indices]
            for i in indices:
                table[i].is_in_4_square = True
            return [deepcopy(square)], table

    return None, table


def minimizing_by_squares(array_of_squares, type_of_formula, num_vars):
    if not array_of_squares:
        return ""
    res = ""
    covered = set()
    for square in array_of_squares:
        square_tuple = tuple(map(tuple, square))
        if square_tuple in covered:
            continue
        res_part = "("
        for number, tup in enumerate(list(zip(*square))):
            if all(x == 0 for x in tup):
                if type_of_formula == "sdnf":
                    res_part += f"!a{number + 1}&"
                elif type_of_formula == "scnf":
                    res_part += f"a{number + 1}|"
            elif all(x == 1 for x in tup):
                if type_of_formula == "sdnf":
                    res_part += f"a{number + 1}&"
                elif type_of_formula == "scnf":
                    res_part += f"!a{number + 1}|"
        res_part = res_part.strip("&").strip("|") + ")"
        if res_part != "()":
            res += res_part + ("|" if type_of_formula == "sdnf" else "&")
            covered.add(square_tuple)
    return res.strip("&").strip("|")