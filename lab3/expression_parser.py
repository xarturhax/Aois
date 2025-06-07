# expression_parser.py
import helpers as hlp


def valid_var(char):
    return char in 'abcdefghijklmnopqrstuvwxyz'


def tokenize_input(expression):
    tokens = []
    position = 0
    while position < hlp.string_length(expression):
        char = hlp.get_char(expression, position)
        if char == ' ':
            position += 1
        elif valid_var(char):
            tokens = hlp.add_item(tokens, char)
            position += 1
        elif char == '-' and position + 1 < hlp.string_length(expression) and hlp.get_char(expression,
                                                                                           position + 1) == '>':
            tokens = hlp.add_item(tokens, '->')
            position += 2
        elif char == '~':
            tokens = hlp.add_item(tokens, '~')
            position += 1
        elif char in '!&|()':
            tokens = hlp.add_item(tokens, char)
            position += 1
        else:
            position += 1
    return tokens


def extract_vars(token_list):
    variables = []
    for token in token_list:
        if valid_var(token) and not hlp.value_in_list(variables, token):
            variables = hlp.add_item(variables, token)
    return hlp.sort_list(variables)


def operator_priority(op):
    priorities = {
        '!': 4,
        '&': 3,
        '|': 2,
        '->': 1,
        '~': 1
    }
    return priorities.get(op, -1)


def infix_to_postfix(tokens):
    output = []
    stack = []

    for token in tokens:
        if valid_var(token):
            output = hlp.add_item(output, token)
        elif token == '(':
            stack = hlp.add_item(stack, token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output = hlp.add_item(output, stack.pop())
            if stack: stack.pop()
        else:
            while stack and stack[-1] != '(' and operator_priority(stack[-1]) >= operator_priority(token):
                output = hlp.add_item(output, stack.pop())
            stack = hlp.add_item(stack, token)

    while stack:
        output = hlp.add_item(output, stack.pop())

    return output