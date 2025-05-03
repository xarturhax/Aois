from .addition import add_twos_complement

def subtract_twos_complement(num1: int, num2: int) -> tuple:
    """Correct subtraction using two's complement"""
    # Subtraction is addition of num1 and -num2
    return add_twos_complement(num1, -num2)