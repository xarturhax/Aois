from src.aois_lab1.binary_representation.direct_code import (
    decimal_to_binary,
    binary_to_decimal,
    get_direct_code
)


def multiply_direct_code(num1: int, num2: int) -> tuple:
    """Correct multiplication in direct code with proper return values"""
    # Determine result sign
    negative = (num1 < 0) ^ (num2 < 0)

    # Work with absolute values
    abs_num1 = abs(num1)
    abs_num2 = abs(num2)

    # Handle zero case
    if abs_num1 == 0 or abs_num2 == 0:
        binary = '0'
        decimal = 0
        direct_code = '0 0'
        return binary, decimal, direct_code

    # Convert to binary strings
    bin1 = decimal_to_binary(abs_num1)
    bin2 = decimal_to_binary(abs_num2)

    # Initialize result
    result = 0

    # Perform multiplication using shift-and-add
    for i, bit in enumerate(reversed(bin2)):
        if bit == '1':
            shifted = abs_num1 << i
            result += shifted

    # Apply sign
    if negative:
        result = -result

    # Convert results
    binary_result = decimal_to_binary(abs(result))
    decimal_result = result
    direct_code_result = get_direct_code(result)

    return binary_result, decimal_result, direct_code_result