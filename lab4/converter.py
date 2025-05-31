from prettytable import PrettyTable


def decimal_to_binary(decimal_number):
    binary_number = ['0'] * 4
    index = len(binary_number) - 1
    if decimal_number < 0:
        decimal_number = -decimal_number
        binary_number[0] = '1'
    while decimal_number > 0 and index >= (1 if binary_number[0] == '1' else 0):
        binary_number[index] = str(decimal_number % 2)
        decimal_number //= 2
        index -= 1
    return ''.join(binary_number)


def d8421_table():
    table = PrettyTable()
    table.field_names = ["Д8421", "Д8421 + 1"]

    for decimal in range(10):
        binary = decimal_to_binary(decimal)
        new_decimal = (decimal + 1) % 10
        new_binary = decimal_to_binary(new_decimal)
        table.add_row([binary, new_binary])

    return table


def create_sdnf_expressions(table, field_names):
    sdnf_expressions = [[] for _ in range(4)]
    for row in table.rows:
        for i in range(4):
            last_element = int(row[1][i])
            if last_element == 1:
                part = []
                for j in range(4):
                    if int(row[0][j]) == 0:
                        part.append(f"!{field_names[j]}")
                    else:
                        part.append(f'{field_names[j]}')
                sdnf_expressions[i].append('  '.join(part))
    return sdnf_expressions