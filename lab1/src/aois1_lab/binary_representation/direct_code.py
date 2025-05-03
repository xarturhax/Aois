def decimal_to_binary(number: int) -> str:
    """Convert decimal to binary string (absolute value)"""
    if number == 0:
        return '0'
    abs_num = abs(number)
    return bin(abs_num)[2:]

def get_direct_code(number: int) -> str:
    """Get direct code representation with sign bit"""
    binary = decimal_to_binary(number)
    sign = '0' if number >= 0 else '1'
    return f"{sign} {binary}"


def binary_to_decimal(binary_str: str) -> int:
    """Convert binary string to decimal number"""
    if not binary_str:
        return 0
    return int(binary_str, 2)