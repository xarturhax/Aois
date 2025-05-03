from .direct_code import decimal_to_binary


def get_ones_complement(number: int) -> str:
    """Get ones' complement (inverse code) representation of a number"""
    if number == 0:
        return '0 0'

    binary = decimal_to_binary(abs(number))
    sign_bit = '0' if number >= 0 else '1'

    if sign_bit == '0':
        return f"{sign_bit} {binary}"

    # For negative numbers, invert all bits except sign
    inverted = ''.join(['1' if bit == '0' else '0' for bit in binary])
    return f"{sign_bit} {inverted}"