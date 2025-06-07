# expression_processor.py
import helpers as hlp


def compute_operator(op, x, y):
    if op == '&':
        return x & y
    if op == '|':
        return x | y
    if op == '->':
        return 0 if x and not y else 1
    if op == '~':
        return 1 if x == y else 0
    return 0


def invert_value(val):
    return 1 - val


def compute_expression(expr, val_dict):
    stack = []
    idx = 0
    while idx < hlp.list_size(expr):
        token = expr[idx]
        if token in 'abcde':
            stack = hlp.add_item(stack, val_dict[token])
        elif token == '!':
            top = stack[hlp.list_size(stack) - 1]
            stack = stack[:hlp.list_size(stack) - 1]
            stack = hlp.add_item(stack, invert_value(top))
        else:
            right = stack[hlp.list_size(stack) - 1]
            stack = stack[:hlp.list_size(stack) - 1]
            left = stack[hlp.list_size(stack) - 1]
            stack = stack[:hlp.list_size(stack) - 1]
            stack = hlp.add_item(stack, compute_operator(token, left, right))
        idx += 1
    return stack[0]


def generate_truth_table(expr, vars):
    outputs = []
    combinations = 1 << hlp.list_size(vars)

    for i in range(combinations):
        current_combo = []
        for j in range(hlp.list_size(vars)):
            shift_amount = hlp.list_size(vars) - j - 1
            bit_val = (i >> shift_amount) & 1
            current_combo = hlp.add_item(current_combo, bit_val)

        val_map = {}
        for k in range(hlp.list_size(vars)):
            val_map[vars[k]] = current_combo[k]

        res = compute_expression(expr, val_map)
        outputs = hlp.add_item(outputs, (current_combo, res))

    return outputs