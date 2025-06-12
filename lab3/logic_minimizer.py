import helpers as hlp
import re
from prettytable import PrettyTable


def create_minterms(table, variables, target_value):
    """Create minterms or maxterms from truth table"""
    terms = []
    for row in table:
        if row[1] == target_value:
            term = []
            for i, var in enumerate(variables):
                term.append((var, row[0][i]))
            terms.append(term)
    return terms


def sort_term(term):
    """Sort variables in term alphabetically"""
    return sorted(term, key=lambda x: x[0])


def terms_equal(term1, term2):
    """Check if two terms are identical"""
    if len(term1) != len(term2):
        return False
    return all(v1 == v2 and val1 == val2
               for (v1, val1), (v2, val2) in zip(sort_term(term1), sort_term(term2)))


def can_combine(term1, term2):
    """Check if two terms can be combined (differ by one variable)"""
    if len(term1) != len(term2):
        return False, None

    diff_count = 0
    diff_var = None
    for (v1, val1), (v2, val2) in zip(sort_term(term1), sort_term(term2)):
        if v1 != v2:
            return False, None
        if val1 != val2:
            diff_count += 1
            diff_var = v1
    return (True, diff_var) if diff_count == 1 else (False, None)


def combine_terms(term, diff_var):
    """Combine two terms by removing the differing variable"""
    return [t for t in term if t[0] != diff_var]


def format_term(term, is_minterm):
    """Format term for display (using ¬ for negation)"""
    if not term:
        return "1" if is_minterm else "0"

    literals = []
    for var, val in sort_term(term):
        if (is_minterm and val == 1) or (not is_minterm and val == 0):
            literals.append(var)
        else:
            literals.append(f"¬{var}")

    if is_minterm:
        return "".join(literals)
    else:
        return f"({'∨'.join(literals)})"


def format_term_compact(term, is_minterm):
    """Format term for display (using ! for negation)"""
    if not term:
        return "1" if is_minterm else "0"

    literals = []
    for var, val in sort_term(term):
        if (is_minterm and val == 1) or (not is_minterm and val == 0):
            literals.append(var)
        else:
            literals.append(f"!{var}")

    if is_minterm:
        return "".join(literals)
    else:
        return f"({'|'.join(literals)})"


def merge_terms(terms, operator):
    """Combine multiple terms into a single expression"""
    if not terms:
        return "0" if operator == " ∨ " else "1"

    # Add parentheses for SKNF terms with multiple literals
    formatted_terms = []
    for term in terms:
        if operator == " ∧ " and "∨" in term and not term.startswith("("):
            formatted_terms.append(f"({term})")
        else:
            formatted_terms.append(term)

    return operator.join(formatted_terms)


def is_covered(implicant, term):
    """Check if term is covered by implicant"""
    for var, val in implicant:
        found = False
        for v, value in term:
            if v == var and val == value:
                found = True
                break
        if not found:
            return False
    return True


def build_coverage_matrix(terms, implicants):
    """Build coverage matrix for prime implicants"""
    return [
        [1 if is_covered(imp, term) else 0
         for imp in implicants]
        for term in terms
    ]


def quine_mccluskey(terms, is_minterm):
    """Perform Quine-McCluskey minimization algorithm"""
    if not terms:
        return [], []

    prime_implicants = []
    current_terms = remove_duplicates(terms)
    steps = []
    step_num = 1

    while True:
        next_terms = []
        marked = [False] * len(current_terms)
        changed = False

        for i in range(len(current_terms)):
            for j in range(i + 1, len(current_terms)):
                term1 = current_terms[i]
                term2 = current_terms[j]
                can_combine_res, diff_var = can_combine(term1, term2)

                if can_combine_res:
                    combined = combine_terms(term1, diff_var)
                    if not contains_term(next_terms, combined):
                        next_terms.append(combined)
                        steps.append(
                            f"Step {step_num}: Combine {format_term(term1, is_minterm)} "
                            f"and {format_term(term2, is_minterm)} → "
                            f"{format_term(combined, is_minterm)}"
                        )
                    marked[i] = marked[j] = True
                    changed = True

        # Add unmarked terms to prime implicants
        for i, term in enumerate(current_terms):
            if not marked[i] and not contains_term(prime_implicants, term):
                prime_implicants.append(term)

        if not changed:
            break

        current_terms = remove_duplicates(next_terms)
        step_num += 1

    return prime_implicants, steps


def select_prime_implicants(terms, prime_implicants):
    """Select essential prime implicants using coverage matrix"""
    if not terms or not prime_implicants:
        return []

    coverage = build_coverage_matrix(terms, prime_implicants)
    uncovered_indices = list(range(len(terms)))
    selected = []

    while uncovered_indices:
        # Find essential prime implicants
        essential_found = False
        for i in uncovered_indices[:]:
            covering = [
                j for j in range(len(prime_implicants))
                if coverage[i][j] == 1 and
                   not contains_term(selected, prime_implicants[j])
            ]

            if len(covering) == 1:
                selected.append(prime_implicants[covering[0]])
                essential_found = True
                # Remove covered terms
                uncovered_indices = [
                    idx for idx in uncovered_indices
                    if not coverage[idx][covering[0]]
                ]  # Fixed this line
                break

        if essential_found:
            continue

        # If no essential found, use greedy selection
        best_imp = None
        max_cover = 0
        for j in range(len(prime_implicants)):
            if contains_term(selected, prime_implicants[j]):
                continue

            cover_count = sum(
                1 for idx in uncovered_indices
                if coverage[idx][j] == 1
            )

            if cover_count > max_cover:
                max_cover = cover_count
                best_imp = prime_implicants[j]

        if best_imp is None:
            break

        selected.append(best_imp)
        uncovered_indices = [
            idx for idx in uncovered_indices
            if not any(
                coverage[idx][j] == 1 and
                terms_equal(prime_implicants[j], best_imp)
                for j in range(len(prime_implicants))
            )
        ]

    return remove_duplicates(selected)


def minimize_expression(terms, is_minterm):
    """Minimize expression using Quine-McCluskey algorithm"""
    prime_implicants, steps = quine_mccluskey(terms, is_minterm)
    minimized = select_prime_implicants(terms, prime_implicants)
    return minimized, steps


def minimize_with_table(terms, is_minterm, original_terms):
    """Minimize expression and return coverage table"""
    prime_implicants, steps = quine_mccluskey(terms, is_minterm)
    minimized = select_prime_implicants(original_terms, prime_implicants)

    table = []
    if prime_implicants and original_terms:
        # Build header
        header = ["Term"]
        header += [format_term_compact(imp, is_minterm) for imp in prime_implicants]
        table.append(header)

        # Build rows
        for term in original_terms:
            row = [format_term_compact(term, is_minterm)]
            row += ["X" if is_covered(imp, term) else "."
                    for imp in prime_implicants]
            table.append(row)

    return minimized, steps, table


def get_kmap_dimensions(num_vars):
    """Get dimensions for Karnaugh map based on number of variables"""
    if num_vars == 1:
        return 1, 2, 0, 1
    elif num_vars == 2:
        return 2, 2, 1, 1
    elif num_vars == 3:
        return 2, 4, 1, 2
    elif num_vars == 4:
        return 4, 4, 2, 2
    elif num_vars == 5:  # Добавлена поддержка 5 переменных
        return 4, 8, 2, 3  # 4 строки, 8 столбцов
    else:
        return None, None, None, None


def gray_code(n):
    """Generate Gray codes for n bits"""
    if n == 0:
        return [""]
    if n == 1:
        return ["0", "1"]
    prev = gray_code(n - 1)
    return ["0" + code for code in prev] + ["1" + code for code in prev[::-1]]


def create_karnaugh_map(terms, variables, is_minterm):
    """Create Karnaugh map for given terms"""
    num_vars = len(variables)
    rows, cols, row_vars, col_vars = get_kmap_dimensions(num_vars)
    if rows is None:
        return None, None

    # Initialize map with 0s (for minterms) or 1s (for maxterms)
    kmap = [[0 if is_minterm else 1 for _ in range(cols)] for _ in range(rows)]

    # Generate Gray codes for rows and columns
    row_codes = gray_code(row_vars)
    col_codes = gray_code(col_vars)

    # Fill the map
    for term in terms:
        row_bits = []
        col_bits = []
        for var in variables:
            val = None
            for v, value in term:
                if v == var:
                    val = value
                    break
            if val is None:
                continue

            if len(row_bits) < row_vars:
                row_bits.append(str(val))
            else:
                col_bits.append(str(val))

        row_str = "".join(row_bits)
        col_str = "".join(col_bits)

        try:
            row_idx = row_codes.index(row_str) if row_vars > 0 else 0
            col_idx = col_codes.index(col_str)
            kmap[row_idx][col_idx] = 1 if is_minterm else 0
        except ValueError:
            continue

    return kmap, (row_codes, col_codes, row_vars, col_vars, variables)


def format_kmap_for_display(kmap, params):
    """Format Karnaugh map for pretty printing"""
    row_codes, col_codes, row_vars, col_vars, variables = params
    pt = PrettyTable()

    # Create header
    if row_vars > 0:
        # Join all row variables for header
        row_vars_str = "".join(variables[:row_vars])
        col_vars_str = "".join(variables[row_vars:])
        header = [f"{row_vars_str}\\{col_vars_str}"]
    else:
        header = [""]

    for code in col_codes:
        header.append(code)
    pt.field_names = header

    # Add rows
    for i in range(len(kmap)):
        row_label = row_codes[i] if i < len(row_codes) else ""
        pt.add_row([row_label] + kmap[i])

    return pt


def minimize_with_kmap(terms, is_minterm, variables):
    """Minimize using Karnaugh map method"""
    kmap, params = create_karnaugh_map(terms, variables, is_minterm)
    minimized, steps = minimize_expression(terms, is_minterm)

    if kmap is None:
        return minimized, steps, [["Karnaugh map not supported for this number of variables"]]

    return minimized, steps, format_kmap_for_display(kmap, params)


# Helper functions
def remove_duplicates(terms):
    """Remove duplicate terms"""
    unique = []
    for term in terms:
        if not contains_term(unique, term):
            unique.append(term)
    return unique


def contains_term(term_list, term):
    """Check if term exists in list"""
    return any(terms_equal(t, term) for t in term_list)
