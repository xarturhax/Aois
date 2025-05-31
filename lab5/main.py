from boolean_minimizer import BooleanMinimizer
from prettytable import PrettyTable


def build_transition_table(n_bits=4):
    """Constructs state transition table for binary counter"""
    bits = [1] * n_bits
    transition_data = []

    for _ in range(2 ** n_bits):
        current_state = bits[:]
        V = 1

        # Calculate T inputs
        T = [0] * n_bits
        T[0] = V
        for i in range(1, n_bits):
            if V == 1 and all(current_state[j] == 0 for j in range(i)):
                T[i] = 1

        # Compute next state and h signals
        next_state = [current_state[i] ^ T[i] for i in range(n_bits)]
        h_signals = [1 if current_state[i] != next_state[i] else 0 for i in range(n_bits)]

        transition_data.append((
            list(reversed(current_state)) + [V],
            list(reversed(h_signals))
        ))
        bits = next_state

    return transition_data


def build_sdnf(transition_data, output_index, input_names):
    """Constructs canonical DNF from truth table"""
    minterms = []

    for inputs, outputs in transition_data:
        if outputs[output_index] == 1:
            literals = [
                var if val == 1 else f"!{var}"
                for var, val in zip(input_names, inputs)
            ]
            minterms.append("(" + "&".join(literals) + ")")

    return " | ".join(minterms) if minterms else "0"


def display_transition_table(data, input_names, output_names):
    """Displays transition table using PrettyTable"""
    table = PrettyTable()
    table.field_names = ["Step"] + input_names + output_names

    for step, (inputs, outputs) in enumerate(data):
        table.add_row([step] + inputs + outputs)

    print("State Transition Table:")
    print(table)
    print()


def minimize_expression(raw_expr, var_mapping, form_type=1):
    """Minimizes boolean expression using BooleanMinimizer"""
    # Convert variables to single letters
    for original, replacement in var_mapping.items():
        raw_expr = raw_expr.replace(original, replacement)

    # Perform minimization
    minimizer = BooleanMinimizer(raw_expr, form_type)
    prime_implicants = minimizer.minimize_calculative()
    minimized_expr = minimizer.implicants_to_string(prime_implicants)

    # Convert back to original variable names
    for replacement, original in var_mapping.items():
        minimized_expr = minimized_expr.replace(original, replacement)

    return minimized_expr


def main():
    # Configuration
    input_vars = ["q4s", "q3s", "q2s", "q1s", "V"]
    output_vars = ["h4", "h3", "h2", "h1"]
    variable_map = {
        'A': 'q4s',
        'B': 'q3s',
        'C': 'q2s',
        'D': 'q1s',
        'E': 'V'
    }
    reverse_map = {v: k for k, v in variable_map.items()}

    # Generate and display transition table
    transition_data = build_transition_table()
    display_transition_table(transition_data, input_vars, output_vars)

    # Process each output function
    for idx, output_name in enumerate(output_vars):
        # Build canonical form
        canonical_form = build_sdnf(transition_data, idx, input_vars)
        print(f"Canonical DNF for {output_name}:")
        print(canonical_form)

        # Minimize expression
        minimized_form = minimize_expression(
            canonical_form,
            reverse_map,
            form_type=1
        )

        print(f"\nMinimized DNF for {output_name}:")
        print(minimized_form.replace(" | ", " ∨ ").replace(" & ", " ∧ "))
        print("-" * 50)


if __name__ == "__main__":
    main()