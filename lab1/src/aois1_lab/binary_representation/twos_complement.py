from .ones_complement import get_ones_complement


def get_twos_complement(number: int) -> str:
    """Get two's complement representation of a number"""
    if number == 0:
        return '0 0'

    ones_complement = get_ones_complement(number)
    sign_bit, bits = ones_complement.split()

    if sign_bit == '0':
        return ones_complement

    # For negative numbers, add 1 to the ones' complement
    bits_list = list(bits)
    carry = 1
    for i in range(len(bits_list) - 1, -1, -1):
        if bits_list[i] == '0' and carry == 1:
            bits_list[i] = '1'
            carry = 0
            break
        elif bits_list[i] == '1' and carry == 1:
            bits_list[i] = '0'

    if carry == 1:
        bits_list.insert(0, '1')

    return f"{sign_bit} {''.join(bits_list)}"