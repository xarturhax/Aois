from src.aois_lab1.binary_representation import (
    direct_code,
    ones_complement,
    twos_complement,
    float_ieee754
)
from src.aois_lab1.arithmetic_operations import (
    addition,
    subtraction,
    multiplication,
    division
)
from src.aois_lab1.utils.validation import validate_integer_input, validate_float_input


def print_menu():
    print("\nMenu:")
    print("1. Convert number to binary representations")
    print("2. Add two numbers (two's complement)")
    print("3. Subtract two numbers (two's complement)")
    print("4. Multiply two numbers (direct code)")
    print("5. Divide two numbers (direct code)")
    print("6. Add two floating-point numbers (IEEE 754)")
    print("7. Exit")


def convert_number():
    try:
        num = validate_integer_input(input("Enter an integer: "))
        print(f"\nNumber entered: {num}")

        # Direct code
        direct = direct_code.get_direct_code(num)
        print(f"Direct code: [{direct}]")

        # Ones' complement
        ones = ones_complement.get_ones_complement(num)
        print(f"Ones' complement: [{ones}]")

        # Two's complement
        twos = twos_complement.get_twos_complement(num)
        print(f"Two's complement: [{twos}]")
    except ValueError as e:
        print(f"Error: {e}")


def add_numbers():
    try:
        num1 = validate_integer_input(input("Enter first number: "))
        num2 = validate_integer_input(input("Enter second number: "))

        print(f"\nNumber 1: {num1}")
        print(f"Direct code: [{direct_code.get_direct_code(num1)}]")
        print(f"Ones' complement: [{ones_complement.get_ones_complement(num1)}]")
        print(f"Two's complement: [{twos_complement.get_twos_complement(num1)}]")

        print(f"\nNumber 2: {num2}")
        print(f"Direct code: [{direct_code.get_direct_code(num2)}]")
        print(f"Ones' complement: [{ones_complement.get_ones_complement(num2)}]")
        print(f"Two's complement: [{twos_complement.get_twos_complement(num2)}]")

        binary_result, decimal_result = addition.add_twos_complement(num1, num2)

        print(f"\nResult: {decimal_result}")
        print(f"Binary result: {binary_result}")
        print(f"Direct code: [{direct_code.get_direct_code(decimal_result)}]")
        print(f"Ones' complement: [{ones_complement.get_ones_complement(decimal_result)}]")
        print(f"Two's complement: [{twos_complement.get_twos_complement(decimal_result)}]")
    except (ValueError, OverflowError) as e:
        print(f"Error: {e}")


def subtract_numbers():
    try:
        num1 = validate_integer_input(input("Enter first number (minuend): "))
        num2 = validate_integer_input(input("Enter second number (subtrahend): "))

        print(f"\nNumber 1: {num1}")
        print(f"Direct code: [{direct_code.get_direct_code(num1)}]")
        print(f"Ones' complement: [{ones_complement.get_ones_complement(num1)}]")
        print(f"Two's complement: [{twos_complement.get_twos_complement(num1)}]")

        print(f"\nNumber 2: {num2}")
        print(f"Direct code: [{direct_code.get_direct_code(num2)}]")
        print(f"Ones' complement: [{ones_complement.get_ones_complement(num2)}]")
        print(f"Two's complement: [{twos_complement.get_twos_complement(num2)}]")

        binary_result, decimal_result = subtraction.subtract_twos_complement(num1, num2)

        print(f"\nResult: {decimal_result}")
        print(f"Binary result: {binary_result}")
        print(f"Direct code: [{direct_code.get_direct_code(decimal_result)}]")
        print(f"Ones' complement: [{ones_complement.get_ones_complement(decimal_result)}]")
        print(f"Two's complement: [{twos_complement.get_twos_complement(decimal_result)}]")
    except (ValueError, OverflowError) as e:
        print(f"Error: {e}")


def multiply_numbers():
    try:
        num1 = validate_integer_input(input("Enter first number: "))
        num2 = validate_integer_input(input("Enter second number: "))

        print(f"\nNumber 1: {num1}")
        print(f"Direct code: [{direct_code.get_direct_code(num1)}]")

        print(f"\nNumber 2: {num2}")
        print(f"Direct code: [{direct_code.get_direct_code(num2)}]")

        binary_result, decimal_result, direct_code_result = multiplication.multiply_direct_code(num1, num2)

        print(f"\nResult: {decimal_result}")
        print(f"Binary result: {binary_result}")
        print(f"Direct code: [{direct_code_result}]")
    except ValueError as e:
        print(f"Error: {e}")


def divide_numbers():
    try:
        num1 = validate_integer_input(input("Enter first number (dividend): "))
        num2 = validate_integer_input(input("Enter second number (divisor): "))

        print(f"\nNumber 1: {num1}")
        print(f"Direct code: [{direct_code.get_direct_code(num1)}]")

        print(f"\nNumber 2: {num2}")
        print(f"Direct code: [{direct_code.get_direct_code(num2)}]")

        binary_result, decimal_result = division.divide_direct_code(num1, num2)

        print(f"\nResult: {decimal_result}")
        print(f"Binary result: {binary_result}")
    except (ValueError, ZeroDivisionError) as e:
        print(f"Error: {e}")


def add_floats():
    try:
        num1 = validate_float_input(input("Enter first floating-point number: "))
        num2 = validate_float_input(input("Enter second floating-point number: "))

        print(f"\nNumber 1: {num1}")
        ieee1 = float_ieee754.float_to_ieee754(num1)
        print(f"IEEE 754 binary32: {ieee1}")

        print(f"\nNumber 2: {num2}")
        ieee2 = float_ieee754.float_to_ieee754(num2)
        print(f"IEEE 754 binary32: {ieee2}")

        # Note: Actual IEEE 754 addition would require bit-level operations
        # For simplicity, we'll use Python's float addition here
        result = num1 + num2
        print(f"\nResult: {result}")
        print(f"IEEE 754 binary32: {float_ieee754.float_to_ieee754(result)}")
    except ValueError as e:
        print(f"Error: {e}")


def main():
    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            convert_number()
        elif choice == '2':
            add_numbers()
        elif choice == '3':
            subtract_numbers()
        elif choice == '4':
            multiply_numbers()
        elif choice == '5':
            divide_numbers()
        elif choice == '6':
            add_floats()
        elif choice == '7':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()