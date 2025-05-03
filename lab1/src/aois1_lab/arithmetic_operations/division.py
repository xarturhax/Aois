from src.aois_lab1.binary_representation.direct_code import decimal_to_binary


def divide_direct_code(num1: int, num2: int, precision: int = 5) -> tuple:
    """Perform precise division with correct binary representation"""
    if num2 == 0:
        raise ZeroDivisionError("Division by zero")

    decimal_result = num1 / num2
    rounded_result = round(decimal_result, precision)

    abs_result = abs(decimal_result)
    int_part = int(abs_result)
    frac_part = abs_result - int_part

    int_binary = decimal_to_binary(int_part)

    frac_binary = ''
    temp = frac_part
    for _ in range(precision):
        temp *= 2
        frac_bit = '1' if temp >= 1.0 else '0'
        frac_binary += frac_bit
        if temp >= 1.0:
            temp -= 1.0

    binary_result = f"{int_binary}.{frac_binary}" if frac_binary else int_binary

    return binary_result, rounded_result