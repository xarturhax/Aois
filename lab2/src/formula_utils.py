from typing import Dict, List
from src.config import LOGIC_OPERATORS

def validate_formula(formula: str) -> bool:
    """Check if the formula contains only valid characters."""
    valid_chars = set("abcde|&!~->()")
    return all(char in valid_chars for char in formula)

def build_cnf(table: Dict[int, List], variables: List[str]) -> str:
    """Construct Conjunctive Normal Form (CNF) from truth table."""
    terms = []
    for i in range(len(table)):
        if table[i][-1] == 0:
            term = [f"({'!' if table[i][j] else ''}{variables[j]})" for j in range(len(variables))]
            terms.append(f"({'|'.join(term)})")
    return "&".join(terms) if terms else ""

def build_dnf(table: Dict[int, List], variables: List[str]) -> str:
    """Construct Disjunctive Normal Form (DNF) from truth table."""
    terms = []
    for i in range(len(table)):
        if table[i][-1] == 1:
            term = [f"({'!' if not table[i][j] else ''}{variables[j]})" for j in range(len(variables))]
            terms.append(f"({'&'.join(term)})")
    return "|".join(terms) if terms else ""

def binary_cnf(table: Dict[int, List], variables: List[str]) -> str:
    """Generate binary form of CNF."""
    terms = [''.join(map(str, table[i][:-1])) for i in range(len(table)) if table[i][-1] == 0]
    return f"&({','.join(terms)})" if terms else "&()"

def decimal_cnf(table: Dict[int, List], variables: List[str]) -> str:
    """Generate decimal form of CNF."""
    terms = [to_decimal(''.join(map(str, table[i][:-1]))) for i in range(len(table)) if table[i][-1] == 0]
    return f"&({','.join(map(str, terms))})" if terms else "&()"

def binary_dnf(table: Dict[int, List], variables: List[str]) -> str:
    """Generate binary form of DNF."""
    terms = [''.join(map(str, table[i][:-1])) for i in range(len(table)) if table[i][-1] == 1]
    return f"|({','.join(terms)})" if terms else "|()"

def decimal_dnf(table: Dict[int, List], variables: List[str]) -> str:
    """Generate decimal form of DNF."""
    terms = [to_decimal(''.join(map(str, table[i][:-1]))) for i in range(len(table)) if table[i][-1] == 1]
    return f"|({','.join(map(str, terms))})" if terms else "|()"

def binary_index(table: Dict[int, List]) -> str:
    """Generate binary index form."""
    return ''.join(str(table[i][-1]) for i in range(len(table)))

def to_decimal(binary: str) -> str:
    """Convert binary string to decimal."""
    return str(sum(2 ** i for i, bit in enumerate(reversed(binary)) if bit == "1"))