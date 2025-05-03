import sys
import os
import pytest

from src.aois_lab1.arithmetic_operations.addition import add_twos_complement
from src.aois_lab1.arithmetic_operations.subtraction import subtract_twos_complement
from src.aois_lab1.arithmetic_operations.multiplication import multiply_direct_code
from src.aois_lab1.arithmetic_operations.division import divide_direct_code
from src.aois_lab1.binary_representation.direct_code import decimal_to_binary, get_direct_code
from src.aois_lab1.binary_representation.ones_complement import get_ones_complement
from src.aois_lab1.binary_representation.twos_complement import get_twos_complement
from src.aois_lab1.binary_representation.float_ieee754 import float_to_ieee754
from src.aois_lab1.utils.conversion import binary_to_decimal, fractional_binary_to_decimal
from src.aois_lab1.utils.validation import validate_integer_input, validate_float_input

class TestDirectCode:

    # Дополнительные тесты для увеличения покрытия
    def test_division_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            divide_direct_code(10, 0)


    def test_binary_conversion(self):
        assert binary_to_decimal('1010') == 10
        assert fractional_binary_to_decimal('101.101') == 5.625

    def test_validation(self):
        assert validate_integer_input('42') == 42
        with pytest.raises(ValueError):
            validate_integer_input('abc')

    def test_decimal_to_binary(self):
        assert decimal_to_binary(5) == '101'
        assert decimal_to_binary(0) == '0'
        assert decimal_to_binary(16) == '10000'

    def test_get_direct_code(self):
        assert get_direct_code(5) == '0 101'
        assert get_direct_code(-3) == '1 11'
        assert get_direct_code(0) == '0 0'


class TestOnesComplement:
    def test_positive_numbers(self):
        assert get_ones_complement(5) == '0 101'

    def test_negative_numbers(self):
        assert get_ones_complement(-5) == '1 010'

    def test_zero(self):
        assert get_ones_complement(0) == '0 0'


class TestTwosComplement:
    def test_positive_numbers(self):
        assert get_twos_complement(5) == '0 101'

    def test_negative_numbers(self):
        assert get_twos_complement(-5) == '1 011'

    def test_zero(self):
        assert get_twos_complement(0) == '0 0'


class TestAddition:
    def test_positive_numbers(self):
        binary, decimal = add_twos_complement(5, 3)
        assert binary == '1000'
        assert decimal == 8

    def test_negative_numbers(self):
        binary, decimal = add_twos_complement(-5, -3)
        assert decimal == -8

    def test_mixed_numbers(self):
        binary, decimal = add_twos_complement(5, -3)
        assert decimal == 2

    def test_addition_edge_cases(self):
        # Тесты для сложения граничных значений
        binary, decimal = add_twos_complement(127, 1)
        assert decimal == 128


class TestSubtraction:
    def test_positive_numbers(self):
        binary, decimal = subtract_twos_complement(10, 4)
        assert decimal == 6

    def test_negative_result(self):
        binary, decimal = subtract_twos_complement(4, 10)
        assert decimal == -6


class TestMultiplication:
    def test_positive_numbers(self):
        binary, decimal, direct = multiply_direct_code(2, 3)
        assert decimal == 6
        assert direct == '0 110'

    def test_negative_numbers(self):
        binary, decimal, direct = multiply_direct_code(-2, 3)
        assert decimal == -6
        assert direct == '1 110'

    def test_zero(self):
        binary, decimal, direct = multiply_direct_code(0, 5)
        assert decimal == 0
        assert direct == '0 0'


class TestDivision:
    def test_positive_numbers(self):
        binary, decimal = divide_direct_code(10, 2)
        assert decimal == 5.0
        assert binary == '101.00000'  # Проверяем целую часть

    def test_negative_numbers(self):
        binary, decimal = divide_direct_code(-10, 2)
        assert decimal == -5.0
        assert binary == '101.00000'  # Проверяем целую часть

    def test_fractional_result(self):
        binary, decimal = divide_direct_code(10, 3)
        # Проверяем точность с учетом правильного округления
        assert abs(decimal - 3.33333) < 1e-5
        # Проверяем формат бинарного результата
        assert binary == '11.01010'  # 3.3125 в двоичной системе
        # Проверяем точность дробной части
        assert len(binary.split('.')[1]) == 5

    def test_division_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            divide_direct_code(10, 0)

class TestFloatIEEE754:
    def test_positive_float(self):
        result = float_to_ieee754(1.0)
        assert result.startswith('001111111000')

    def test_negative_float(self):
        result = float_to_ieee754(-1.0)
        assert result.startswith('101111111000')

    def test_float_conversion_edge_cases(self):
        # Тест для +0.0
        assert float_to_ieee754(0.0) == '0' * 32

        # Тест для -0.0 (исправленный)
        negative_zero = float_to_ieee754(-0.0)
        assert negative_zero[0] == '1', "Знаковый бит должен быть 1 для -0.0"
        assert negative_zero[1:] == '0' * 31, "Остальные биты должны быть нулями"

        # Дополнительная проверка для 1.0
        assert float_to_ieee754(1.0)[:12] == '001111111000'
