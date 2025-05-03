from src.aois_lab1.binary_representation.twos_complement import get_twos_complement
from src.aois_lab1.binary_representation.direct_code import binary_to_decimal


def add_twos_complement(num1: int, num2: int) -> tuple:
    """Correctly add two numbers in two's complement representation"""

    # Convert numbers to binary strings without sign bits
    def to_binary(n):
        return bin(abs(n))[2:] if n != 0 else '0'

    max_len = max(len(to_binary(num1)), len(to_binary(num2))) + 1

    # Prepare binary numbers with equal length
    bin1 = to_binary(num1).zfill(max_len)
    bin2 = to_binary(num2).zfill(max_len)

    # Perform binary addition
    result = []
    carry = 0
    for a, b in zip(reversed(bin1), reversed(bin2)):
        sum_bits = int(a) + int(b) + carry
        result.append(str(sum_bits % 2))
        carry = sum_bits // 2

    if carry:
        result.append('1')

    binary_result = ''.join(reversed(result))
    decimal_result = num1 + num2  # For verification

    # Handle overflow
    if num1 > 0 and num2 > 0 and decimal_result < 0:
        raise OverflowError("Positive overflow")
    elif num1 < 0 and num2 < 0 and decimal_result > 0:
        raise OverflowError("Negative overflow")

    return binary_result, decimal_result