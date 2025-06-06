from typing import List, Dict, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import itertools
from itertools import product
import re

class Operator(Enum):
    NOT = '!'
    AND = '&'
    OR = '|'
    IMPLIES = '>'
    EQUIVALENT = '~'

@dataclass
class ExpressionNode:
    value: str
    left: 'ExpressionNode' = None
    right: 'ExpressionNode' = None

class ExpressionParser:
    def __init__(self):
        self.operators = {
            '!': 3,
            '&': 2,
            '|': 1,
            '>': 0,
            '~': 0
        }

    def parse(self, expression: str) -> ExpressionNode:
        tokens = self._tokenize(expression)
        return self._build_tree(tokens)

    def _tokenize(self, expression: str) -> List[str]:
        tokens = []
        i = 0
        while i < len(expression):
            if expression[i].isalpha():
                tokens.append(expression[i])
            elif expression[i] in self.operators or expression[i] in '()':
                tokens.append(expression[i])
            i += 1
        return tokens

    def _build_tree(self, tokens: List[str]) -> ExpressionNode:
        if not tokens:
            return None
        
        if len(tokens) == 1:
            return ExpressionNode(tokens[0])
        
        # Handle negation
        if tokens[0] == '!':
            return ExpressionNode('!', self._build_tree(tokens[1:]))
        
        # Find the operator with lowest precedence
        min_prec = float('inf')
        min_idx = -1
        
        for i, token in enumerate(tokens):
            if token in self.operators and self.operators[token] < min_prec:
                min_prec = self.operators[token]
                min_idx = i
        
        if min_idx == -1:
            return ExpressionNode(tokens[0])
        
        return ExpressionNode(
            tokens[min_idx],
            self._build_tree(tokens[:min_idx]),
            self._build_tree(tokens[min_idx + 1:])
        )

class ExpressionEvaluator:
    @staticmethod
    def evaluate(node: ExpressionNode, values: Dict[str, bool]) -> bool:
        if node is None:
            return False
            
        if node.value.isalpha():
            return values[node.value]
            
        if node.value == '!':
            return not ExpressionEvaluator.evaluate(node.left, values)
            
        left_val = ExpressionEvaluator.evaluate(node.left, values)
        right_val = ExpressionEvaluator.evaluate(node.right, values)
        
        if node.value == '&':
            return left_val and right_val
        elif node.value == '|':
            return left_val or right_val
        elif node.value == '>':
            return (not left_val) or right_val
        elif node.value == '~':
            return left_val == right_val
            
        raise ValueError(f"Unknown operator: {node.value}")

def replace_implication_equivalence(expr):
    expr = expr.replace(' ', '')  # Удаляем все пробелы для корректной работы регулярных выражений
    print(f"Исходное выражение: {expr}")  # отладка
    def process_brackets(s):
        res = ''
        i = 0
        while i < len(s):
            if s[i] == '(':  # нашли открывающую скобку
                depth = 1
                j = i + 1
                while j < len(s) and depth > 0:
                    if s[j] == '(': depth += 1
                    if s[j] == ')': depth -= 1
                    j += 1
                # рекурсивно обрабатываем содержимое скобок
                inner = process_brackets(s[i+1:j-1])
                res += '(' + inner + ')'
                i = j
            else:
                res += s[i]
                i += 1
        # После обработки скобок — преобразуем импликацию и эквиваленцию на этом уровне
        print(f"До замены: {res}")  # отладка
        # Новый шаблон: ищем левый и правый операнд как выражение в скобках или последовательность символов
        pattern_imp = re.compile(r'(\([^(]*\)|[\w]+)>(\([^(]*\)|[\w]+)')
        imp_count = 0
        while '>' in res:
            res_new = pattern_imp.sub(lambda m: f'(not {m.group(1)}) or {m.group(2)}', res)
            if res_new == res:
                break
            res = res_new
            imp_count += 1
            if imp_count > 10:
                raise ValueError('Слишком сложная или некорректная импликация в выражении!')
        print(f"После импликации: {res}")  # отладка
        # Обработка эквиваленции: разбиваем выражение по ~ и преобразуем каждую часть
        if '~' in res:
            parts = res.split('~')
            if len(parts) == 2:
                left, right = parts
                res = f'(({left}) and ({right})) or (not ({left}) and not ({right}))'
        print(f"После эквиваленции: {res}")  # отладка
        if '>' in res or '~' in res:
            raise ValueError('Не удалось полностью преобразовать выражение!')
        return res
    return process_brackets(expr)

def eval_expr(expr: str) -> int:
    expr = expr.replace(' ', '')
    if expr.startswith('(') and expr.endswith(')'):
        depth = 0
        for i, c in enumerate(expr):
            if c == '(': depth += 1
            if c == ')': depth -= 1
            if depth == 0 and i != len(expr) - 1:
                break
        else:
            return eval_expr(expr[1:-1])
    def split_outside(expr, op):
        depth = 0
        for i in range(len(expr)-1, -1, -1):
            if expr[i] == ')': depth += 1
            elif expr[i] == '(': depth -= 1
            elif depth == 0 and expr[i] == op:
                return expr[:i], expr[i+1:]
        return None
    res = split_outside(expr, '~')
    if res:
        left, right = res
        l, r = eval_expr(left), eval_expr(right)
        return int((l and r) or ((not l) and (not r)))
    res = split_outside(expr, '>')
    if res:
        left, right = res
        l, r = eval_expr(left), eval_expr(right)
        return int((not l) or r)
    res = split_outside(expr, '|')
    if res:
        left, right = res
        l, r = eval_expr(left), eval_expr(right)
        return int(l or r)
    res = split_outside(expr, '&')
    if res:
        left, right = res
        l, r = eval_expr(left), eval_expr(right)
        return int(l and r)
    if expr.startswith('!'):
        return int(not eval_expr(expr[1:]))
    if expr in ('0', '1'):
        return int(expr)
    raise ValueError(f'Не удалось разобрать выражение: {expr}')

def generate_truth_table(expression: str) -> list:
    if not validate_input(expression):
        raise ValueError("Некорректное выражение. Используйте только переменные a, b, c, операторы !, &, |, >, ~ и скобки ()")
    variables = sorted(set(c for c in expression if c in 'abc'))
    if not variables:
        raise ValueError("Выражение должно содержать хотя бы одну переменную (a, b или c)")
    truth_table = []
    for values in product([0, 1], repeat=len(variables)):
        row = dict(zip(variables, values))
        expr = expression
        for var, val in row.items():
            expr = expr.replace(var, str(val))
        # Не заменяем операторы на and/or/not!
        try:
            result = eval_expr(expr)
            row['result'] = result
            truth_table.append(row)
        except Exception as e:
            raise ValueError(f"Ошибка при вычислении выражения: {expr} => {e}")
    return truth_table

def print_truth_table(truth_table: List[Dict]) -> None:
    if not truth_table:
        return
    
    # Получаем переменные из первой строки
    variables = [var for var in truth_table[0].keys() if var != 'result']
    
    # Выводим заголовок
    header = " | ".join(variables + ["F"])
    print(header)
    print("-" * len(header))
    
    # Выводим строки
    for row in truth_table:
        values = [str(row[var]) for var in variables] + [str(row['result'])]
        print(" | ".join(values))

def is_balanced(formula: str) -> bool:
    """Проверяет баланс скобок в формуле."""
    stack = []
    for char in formula:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:  # Если стек пуст, значит нет открывающей скобки
                return False
            stack.pop()
    return len(stack) == 0  # Если стек пуст, значит все скобки сбалансированы

def validate_input(formula: str) -> bool:
    # Проверяем баланс скобок
    if not is_balanced(formula):
        return False
    
    # Проверяем допустимые символы
    valid_chars = set('abc!&|()~> ')
    if not all(c in valid_chars for c in formula):
        return False
    
    # Проверяем, что формула не пустая
    if not formula.strip():
        return False
    
    # Проверяем, что формула содержит хотя бы одну переменную
    if not any(c in 'abc' for c in formula):
        return False
    
    # Проверяем, что операторы используются правильно
    formula = formula.replace(' ', '')
    i = 0
    while i < len(formula):
        if formula[i] == '!':
            if i + 1 >= len(formula) or formula[i + 1] not in 'abc(':
                return False
        elif formula[i] in '&|>~':
            if i + 1 >= len(formula) or formula[i + 1] not in 'abc!(':
                return False
        elif formula[i] in 'abc':
            if i + 1 < len(formula) and formula[i + 1] not in '&|>~)':
                return False
        i += 1
    
    return True 