from expression_parser import tokenize_input, extract_vars, infix_to_postfix
from expression_processor import generate_truth_table
from logic_minimizer import (create_minterms, minimize_expression, minimize_with_table,
merge_terms, minimize_with_kmap,format_term_compact)
import helpers as hlp
from prettytable import PrettyTable


def display_truth_table(table, variables, expression):
    pt = PrettyTable()
    pt.field_names = variables + [expression]
    for row in table:
        pt.add_row(list(row[0]) + [row[1]])
    print("\n=== TRUTH TABLE ===")
    print(pt)


def display_original_forms(sdnf, sknf):
    print("\n=== ORIGINAL FORMS ===")
    print(f"SDNF: {sdnf if sdnf else '0'}")
    print(f"SKNF: {sknf if sknf else '1'}")


def display_minimization(title, steps, result):
    print(f"\n=== {title.upper()} ===")
    if not steps:
        print("No minimization needed - already minimal")
    else:
        print("Minimization steps:")
        for i, step in enumerate(steps, 1):
            print(f"{i}. {step}")
    print(f"\nMinimized form: {result}")


def display_coverage(title, steps, table, result):
    print(f"\n=== {title.upper()} ===")
    if steps:
        print("Minimization steps:")
        for i, step in enumerate(steps, 1):
            print(f"{i}. {step}")

    if table and len(table) > 1:
        print("\nCoverage Table:")
        pt = PrettyTable()
        pt.field_names = table[0]
        for row in table[1:]:
            pt.add_row(row)
        print(pt)
    elif not table:
        print("No coverage table generated")

    print(f"\nResult: {result}")


def display_kmap(title, kmap, result):
    print(f"\n=== {title.upper()} ===")
    if isinstance(kmap, PrettyTable):
        print(kmap)
    elif isinstance(kmap, list):
        print("\n".join([" ".join(row) for row in kmap]))
    else:
        print("Karnaugh map not available for this case")
    print(f"\nMinimized form: {result}")


def check_trivial_cases(table):
    all_zeros = all(row[1] == 0 for row in table)
    all_ones = all(row[1] == 1 for row in table)

    if all_zeros:
        print("\nThe function is always FALSE (0)")
        return True
    elif all_ones:
        print("\nThe function is always TRUE (1)")
        return True
    return False


def run_program():
    print("=== LOGIC EXPRESSION MINIMIZER ===")
    expression = input("Enter logical expression: ")

    try:
        # Parse and validate input
        tokens = tokenize_input(expression)
        variables = extract_vars(tokens)
        variables = hlp.sort_list(variables)

        if hlp.list_size(variables) > 3:
            print("\nWarning: Karnaugh maps are only supported for up to 3 variables")
        if not variables:
            print("Error: No variables found in expression")
            return

        # Generate truth table
        postfix = infix_to_postfix(tokens)
        truth_table = generate_truth_table(postfix, variables)

        # Display truth table
        display_truth_table(truth_table, variables, expression)

        # Check for trivial cases
        if check_trivial_cases(truth_table):
            return

        # Create canonical forms
        minterms = create_minterms(truth_table, variables, 1)
        maxterms = create_minterms(truth_table, variables, 0)

        # Original forms
        sdnf_initial = merge_terms([format_term_compact(t, True) for t in minterms], " ∨ ") if minterms else "0"
        sknf_initial = merge_terms([format_term_compact(t, False) for t in maxterms], " ∧ ") if maxterms else "1"
        display_original_forms(sdnf_initial, sknf_initial)

        # SDNF Minimization
        min_sdnf, sdnf_steps = minimize_expression(minterms, True)
        sdnf_result = merge_terms([format_term_compact(t, True) for t in min_sdnf], " ∨ ") if min_sdnf else "0"
        display_minimization("SDNF MINIMIZATION (CALCULATION)", sdnf_steps, sdnf_result)

        # SKNF Minimization
        min_sknf, sknf_steps = minimize_expression(maxterms, False)
        sknf_result = merge_terms([format_term_compact(t, False) for t in min_sknf], " ∧ ") if min_sknf else "1"
        display_minimization("SKNF MINIMIZATION (CALCULATION)", sknf_steps, sknf_result)

        # SDNF Table Method
        min_sdnf_tbl, sdnf_tbl_steps, sdnf_table = minimize_with_table(minterms, True, minterms)
        sdnf_tbl_result = merge_terms([format_term_compact(t, True) for t in min_sdnf_tbl],
                                      " ∨ ") if min_sdnf_tbl else "0"
        display_coverage("SDNF TABLE METHOD", sdnf_tbl_steps, sdnf_table, sdnf_tbl_result)

        # SKNF Table Method
        min_sknf_tbl, sknf_tbl_steps, sknf_table = minimize_with_table(maxterms, False, maxterms)
        sknf_tbl_result = merge_terms([format_term_compact(t, False) for t in min_sknf_tbl],
                                      " ∧ ") if min_sknf_tbl else "1"
        display_coverage("SKNF TABLE METHOD", sknf_tbl_steps, sknf_table, sknf_tbl_result)

        # SDNF Karnaugh Map
        min_sdnf_kmap, sdnf_kmap_steps, sdnf_kmap = minimize_with_kmap(minterms, True, variables)
        sdnf_kmap_result = merge_terms([format_term_compact(t, True) for t in min_sdnf_kmap],
                                       " ∨ ") if min_sdnf_kmap else "0"
        display_kmap("SDNF KARNAUGH MAP", sdnf_kmap, sdnf_kmap_result)

        # SKNF Karnaugh Map
        min_sknf_kmap, sknf_kmap_steps, sknf_kmap = minimize_with_kmap(maxterms, False, variables)
        sknf_kmap_result = merge_terms([format_term_compact(t, False) for t in min_sknf_kmap],
                                       " ∧ ") if min_sknf_kmap else "1"
        display_kmap("SKNF KARNAUGH MAP", sknf_kmap, sknf_kmap_result)

    except Exception as e:
        print(f"\nERROR: {str(e)}")
    finally:
        print("\n=== PROGRAM FINISHED ===")


if __name__ == "__main__":
    run_program()
