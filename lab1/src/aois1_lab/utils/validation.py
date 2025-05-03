def validate_integer_input(input_str: str) -> int:
    """Validate and convert user input to integer"""
    try:
        return int(input_str)
    except ValueError:
        raise ValueError("Invalid input. Please enter an integer.")

def validate_float_input(input_str: str) -> float:
    """Validate and convert user input to float"""
    try:
        return float(input_str)
    except ValueError:
        raise ValueError("Invalid input. Please enter a number.")