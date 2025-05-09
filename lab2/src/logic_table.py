from typing import List, Tuple
from src.config import LOGIC_OPERATORS, PRECEDENCE, INITIAL_STATE, INCREMENT_STATE
import re

def to_postfix(expression: str) -> str:
    """Convert infix logical expression to postfix notation."""
    output = []
    op_stack = []
    operators = LOGIC_OPERATORS

    for char in expression.replace("-", "").replace(" ", ""):
        if char == "(":
            op_stack.append(char)
        elif char == ")":
            while op_stack and op_stack[-1] != "(":
                output.append(op_stack.pop())
            if op_stack and op_stack[-1] == "(":
                op_stack.pop()  # Remove '('
        elif char in operators:
            while (op_stack and op_stack[-1] != "(" and
                   PRECEDENCE.get(op_stack[-1], 0) >= PRECEDENCE.get(char, 0)):
                output.append(op_stack.pop())
            op_stack.append(char)
        else:
            output.append(char)

    while op_stack:
        if op_stack[-1] != "(":
            output.append(op_stack.pop())
        else:
            op_stack.pop()  # Remove stray '('

    result = "".join(output)
    # print(f"Postfix: {result}")  # Debug output
    return result

def evaluate_expression(values: List[int], postfix: str, vars_list: List[str]) -> int:
    """Evaluate a postfix expression with given variable values."""
    stack = []
    var_map = {var: val for var, val in zip(vars_list, values)}

    for char in postfix:
        if char in var_map:
            stack.append(var_map[char])
        elif char in LOGIC_OPERATORS:
            if char == "!":
                if not stack:
                    raise ValueError("Invalid postfix expression: empty stack for unary operator")
                val = stack.pop()
                stack.append(0 if val else 1)
            else:
                if len(stack) < 2:
                    raise ValueError(f"Invalid postfix expression: insufficient operands for {char}")
                b, a = stack.pop(), stack.pop()
                if char == "&":
                    stack.append(1 if a and b else 0)
                elif char == "|":
                    stack.append(1 if a or b else 0)
                elif char == ">":
                    stack.append(0 if a and not b else 1)
                elif char == "~":
                    stack.append(1 if a == b else 0)
        # print(f"Stack after {char}: {stack}")  # Debug output
    if len(stack) != 1:
        raise ValueError(f"Invalid postfix expression: final stack size {len(stack)}")
    return stack.pop()

def generate_truth_table(expression: str, display: bool = True) -> Tuple[dict, List]:
    """Generate truth table for a logical expression."""
    postfix = to_postfix(expression)
    vars_list = sorted(set(re.findall(r"[a-zA-Z]", postfix)))
    if display:
        print_table_header(vars_list)

    table = {i: [] for i in range(2 ** len(vars_list))}
    current_state = INITIAL_STATE[-len(vars_list):]

    for i in range(len(table)):
        table[i] = list(current_state) + [evaluate_expression(current_state, postfix, vars_list)]
        if display:
            print(f"{' | '.join(map(str, table[i]))} |")
        current_state = next_state(current_state, INCREMENT_STATE[-len(vars_list):])

    return table, vars_list

def next_state(current: List[int], increment: List[int]) -> List[int]:
    """Generate next binary state for truth table."""
    result = []
    carry = 0
    for a, b in zip(current[::-1], increment[::-1]):
        total = a + b + carry
        result.insert(0, total % 2)
        carry = total // 2
    if carry:
        result.insert(0, 1)
    return result

def print_table_header(vars_list: List[str]) -> None:
    """Display truth table header."""
    header = f"{' | '.join(vars_list)} | Result"
    print(f"\n{header}\n{'-' * len(header)}")