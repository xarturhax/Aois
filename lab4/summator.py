from prettytable import PrettyTable
import itertools


def truth_table(input_variables):
    table = PrettyTable()
    table.field_names = input_variables + ['S', 'C(out)']
    combinations = list(itertools.product([0, 1], repeat=len(input_variables)))

    for combo in combinations:
        row = list(combo)
        a_value, b_value, cin_value = combo
        total = a_value + b_value + cin_value
        if total == 1:
            s_value = 1
            c_out_value = 0
        elif total == 2:
            s_value = 0
            c_out_value = 1
        elif total == 3:
            s_value = 1
            c_out_value = 1
        else:
            s_value = 0
            c_out_value = 0
        row.append(s_value)
        row.append(c_out_value)
        table.add_row(row)
    return table, table.field_names


def create_sdnf(table, field_names, key):
    sdnf_parts = []
    for index, row in enumerate(table.rows, start=1):
        if key == 'sum':
            last_element = int(row[-2])
        else:
            last_element = int(row[-1])
        if last_element == 1:
            part = []
            for i in range(3):
                if int(row[i]) == 0:
                    part.append(f"!{field_names[i]}")
                else:
                    part.append(f'{field_names[i]}')
            sdnf_parts.append(' '.join(part))
    return sdnf_parts


def merge_parts(parts):
    merged = []
    used = set()
    for i in range(len(parts)):
        part1 = parts[i].split()
        for j in range(i + 1, len(parts)):
            part2 = parts[j].split()
            if len(part1) != len(part2):
                continue
            different_var = [(x, y) for x, y in zip(part1, part2) if x != y]
            if len(different_var) == 1 and (
                    (different_var[0][0].startswith('!') and different_var[0][1] == different_var[0][0][1:]) or
                    (different_var[0][1].startswith('!') and different_var[0][0] == different_var[0][1][1:])
            ):
                differences = [x != y for x, y in zip(part1, part2)]
                merged_part = [x if not diff else '' for x, diff in zip(part1, differences)]
                merged.append(' '.join(filter(bool, merged_part)))
                used.add(i)
                used.add(j)
    for k in range(len(parts)):
        if k not in used:
            merged.append(parts[k])

    unique_elements = set()
    final_result = []

    for elem in merged:
        if elem not in unique_elements:
            unique_elements.add(elem)
            final_result.append(elem)

    return final_result


def merging(sdnf_parts):
    current_parts = sdnf_parts
    while True:
        new_parts = merge_parts(current_parts)
        if new_parts == current_parts:
            break
        current_parts = new_parts
    return current_parts


def format_str(parts):
    return " ∨ ".join(f'({t})' for t in parts) if parts else None