from src.formula_utils import *
from src.logic_table import *

def display_results(formula: str) -> None:
    """Process a logical formula and display its SKNF, SDNF, and index forms."""
    if not validate_formula(formula):
        raise ValueError("Invalid formula entered!")

    truth_data, var_list = generate_truth_table(formula)

    # Helper to format and print results
    def print_section(title: str, value: str) -> None:
        print(f"{'=' * 50}\n{title}: {value}")

    print_section("CNF (SKNF)", build_cnf(truth_data, var_list))
    print_section("DNF (SDNF)", build_dnf(truth_data, var_list))
    print_section("CNF Binary", binary_cnf(truth_data, var_list))
    print_section("CNF Decimal", decimal_cnf(truth_data, var_list))
    print_section("DNF Binary", binary_dnf(truth_data, var_list))
    print_section("DNF Decimal", decimal_dnf(truth_data, var_list))
    print_section("Index Binary", binary_index(truth_data))
    print_section("Index Decimal", to_decimal(binary_index(truth_data)))

def run():
    """Entry point to get user input and process the formula."""
    user_input = input("Enter a logical formula: ")
    display_results(user_input)

if __name__ == "__main__":
    run()