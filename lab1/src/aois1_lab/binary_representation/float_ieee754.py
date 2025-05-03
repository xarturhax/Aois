def float_to_ieee754(number: float) -> str:
    """Улучшенная версия с обработкой -0.0"""
    if number == 0.0:
        return '1' + '0' * 31 if str(number)[0] == '-' else '0' * 32

    # Остальная реализация...
    sign_bit = '1' if number < 0 else '0'
    abs_number = abs(number)

    # Separate integer and fractional parts
    integer_part = int(abs_number)
    fractional_part = abs_number - integer_part

    # Convert integer part to binary
    int_binary = bin(integer_part)[2:] if integer_part != 0 else '0'

    # Convert fractional part to binary
    frac_binary = ''
    for _ in range(24):  # Maximum precision for 32-bit float
        fractional_part *= 2
        bit = int(fractional_part)
        frac_binary += str(bit)
        fractional_part -= bit
        if fractional_part == 0:
            break

    # Combine integer and fractional parts
    combined = int_binary + frac_binary

    # Normalize and find exponent
    if integer_part != 0:
        # Normalized number
        exponent = len(int_binary) - 1
        mantissa = combined[1:24]  # 23 bits
    else:
        # Subnormal number - find first 1 in fractional part
        first_one = combined.find('1')
        if first_one == -1:
            # Zero
            return '0' * 32
        exponent = -first_one - 1
        mantissa = combined[first_one + 1:first_one + 24]

    # Calculate biased exponent
    biased_exponent = exponent + 127
    exponent_bits = bin(biased_exponent)[2:].zfill(8)

    # Ensure mantissa is 23 bits
    mantissa = mantissa.ljust(23, '0')[:23]

    return sign_bit + exponent_bits + mantissa