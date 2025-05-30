from priority import PRIORITY, OPS


def reversed_polish_notation(formula):
    output = []
    stack = []
    i = 0
    while i < len(formula):
        char = formula[i]

        # Handle variables
        if char.isalpha():
            output.append(char)
            i += 1
        # Handle negation
        elif char == '!':
            # Check if next character is a variable or opening parenthesis
            if i + 1 < len(formula) and (formula[i + 1].isalpha() or formula[i + 1] == '('):
                stack.append(char)
            else:
                raise ValueError("Invalid formula: misplaced negation")
            i += 1
        # Handle operators
        elif char in OPS:
            while (stack and stack[-1] != '(' and
                   PRIORITY.get(stack[-1], 0) >= PRIORITY.get(char, 0)):
                output.append(stack.pop())
            stack.append(char)
            i += 1
        # Handle opening parenthesis
        elif char == '(':
            stack.append(char)
            i += 1
        # Handle closing parenthesis
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack and stack[-1] == '(':
                stack.pop()  # Remove '('
            else:
                raise ValueError("Mismatched parentheses")
            # Handle negation before parenthesis, e.g., !(...)
            if stack and stack[-1] == '!':
                output.append(stack.pop())
            i += 1
        else:
            raise ValueError(f"Invalid character: {char}")

    # Pop remaining operators
    while stack:
        if stack[-1] == '(':
            raise ValueError("Mismatched parentheses")
        output.append(stack.pop())

    return ''.join(output)


def find_result(row, formula, variables):
    stack = []
    rpn = reversed_polish_notation(formula)

    for char in rpn:
        if char.isalpha():
            # Map variable to its value in the row
            idx = variables.index(char)
            stack.append(row[idx])
        elif char == '!':
            if not stack:
                raise ValueError("Invalid RPN: not enough operands for NOT")
            operand = stack.pop()
            stack.append(1 - operand)  # NOT
        elif char in OPS:
            if len(stack) < 2:
                raise ValueError(f"Invalid RPN: not enough operands for {char}")
            b = stack.pop()
            a = stack.pop()
            if char == '&':
                stack.append(a & b)
            elif char == '|':
                stack.append(a | b)
            elif char == '>':
                stack.append(1 if a == 0 or b == 1 else 0)  # Implication
            elif char == '~':
                stack.append(1 if a == b else 0)  # Equivalence
        else:
            raise ValueError(f"Invalid RPN character: {char}")

    if len(stack) != 1:
        raise ValueError("Invalid RPN: too many operands")
    return stack[0]


def true_table(formula):
    # Extract unique variables
    variables = sorted(set(c for c in formula if c.isalpha()))
    n = len(variables)
    table = {}

    # Generate all possible combinations
    for i in range(2 ** n):
        row = []
        for j in range(n):
            row.append((i >> (n - 1 - j)) & 1)
        table[i] = row
        # Calculate result
        table[i].append(find_result(row, formula, variables))

    return table, variables