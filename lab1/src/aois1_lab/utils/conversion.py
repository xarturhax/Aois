def binary_to_decimal(binary_str: str) -> int:
    """Convert binary string to decimal"""
    return int(binary_str, 2) if binary_str else 0

def fractional_binary_to_decimal(binary_str: str) -> float:
    """Convert fractional binary string to decimal number"""
    if '.' not in binary_str:
        return float(binary_to_decimal(binary_str))

    integer_part, fractional_part = binary_str.split('.')
    decimal = binary_to_decimal(integer_part)

    for i, bit in enumerate(fractional_part, 1):
        decimal += int(bit) * (2 ** -i)

    return decimal