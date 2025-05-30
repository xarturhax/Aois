def calculation_tabular_method(prime_implicants, subsumed_implicants, key=None):
    if not subsumed_implicants:
        return prime_implicants
    table = create_table(prime_implicants, subsumed_implicants)
    filled_columns = [False] * len(table[0])
    minimized_implicants = get_minimized_implicants(prime_implicants, table, filled_columns)
    print_table(prime_implicants, subsumed_implicants, table, key)
    if len(subsumed_implicants) and len(prime_implicants) == 1:
        return subsumed_implicants
    return minimized_implicants


def create_table(prime_implicants, subsumed_implicants):
    table = []
    for implicant in prime_implicants:
        row = []
        for pi in subsumed_implicants:
            # Check if prime implicant covers subsumed implicant
            if set(implicant).issubset(set(pi)):
                row.append(True)
            else:
                row.append(False)
        table.append(row)
    return table


def get_minimized_implicants(prime_implicants, table, filled_columns):
    minimized_implicants = []
    num_columns = len(table[0])

    # Find essential prime implicants (columns with a single True)
    for j in range(num_columns):
        column = [table[i][j] for i in range(len(table))]
        if column.count(True) == 1:
            idx = column.index(True)
            if prime_implicants[idx] not in minimized_implicants:
                minimized_implicants.append(prime_implicants[idx])
            for k in range(num_columns):
                if table[idx][k]:
                    filled_columns[k] = True

    # If not all columns are filled, add additional implicants
    while not all(filled_columns):
        max_coverage = 0
        best_implicant = None
        best_idx = -1
        for i in range(len(prime_implicants)):
            if prime_implicants[i] in minimized_implicants:
                continue
            coverage = sum(table[i][j] for j in range(num_columns) if not filled_columns[j])
            if coverage > max_coverage:
                max_coverage = coverage
                best_implicant = prime_implicants[i]
                best_idx = i
        if best_implicant:
            minimized_implicants.append(best_implicant)
            for j in range(num_columns):
                if table[best_idx][j]:
                    filled_columns[j] = True
        else:
            break  # No more implicants to add

    return minimized_implicants


def print_table(prime_implicants, subsumed_implicants, table, key):
    if not prime_implicants or not subsumed_implicants:
        return
    implicant_width = max(len(' '.join(implicant)) for implicant in prime_implicants)
    header_width = 12 if key == "sdnf" else 11
    column_width = max(header_width, implicant_width + 2)
    print(' ' * column_width, end='')
    sign = "&" if key == "sdnf" else "|"
    for implicant in subsumed_implicants:
        print(f"| {sign.join(implicant).ljust(column_width - 1)} ", end='')
    print()
    for index, row in enumerate(table):
        print(f" {sign.join(prime_implicants[index]).ljust(column_width)} ", end='')
        for column in row:
            if column:
                print(f"| {'x'.center(column_width - 2)} ", end='')
            else:
                print(f"| {' '.center(column_width - 2)} ", end='')
        print("|")