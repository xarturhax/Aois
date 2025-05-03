from src.aois_lab1.binary_representation.direct_code import decimal_to_binary


def divide_direct_code(num1: int, num2: int, precision: int = 5) -> tuple:
    """Улучшенная версия с более точными вычислениями"""
    if num2 == 0:
        raise ZeroDivisionError("Division by zero")

    # Увеличиваем точность вычислений
    abs_num1 = abs(num1)
    abs_num2 = abs(num2)
    integer_part = abs_num1 // abs_num2
    remainder = abs_num1 % abs_num2

    fractional_part = 0.0
    for i in range(1, precision + 1):
        remainder *= 10
        fractional_part += (remainder // abs_num2) * (10 ** -i)
        remainder %= abs_num2

    result = integer_part + fractional_part
    if (num1 < 0) ^ (num2 < 0):
        result = -result

    binary = decimal_to_binary(int(result))
    return binary, round(result, precision)