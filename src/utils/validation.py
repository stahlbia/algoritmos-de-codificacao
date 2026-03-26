"""
Input validation functions.
"""

from typing import Union, List, Any


def validate_positive_int(value: Any, name: str = "value") -> int:
    """
    Validate that value is a positive integer.

    Args:
        value: Value to validate
        name: Name of value for error messages

    Returns:
        Validated integer

    Raises:
        ValueError: If value is not a positive integer
        TypeError: If value is not an integer
    """
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an integer, got {type(value).__name__}")
    
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")
    
    return value


def validate_non_negative_int(value: Any, name: str = "value") -> int:
    """
    Validate that value is a non-negative integer.

    Args:
        value: Value to validate
        name: Name of value for error messages

    Returns:
        Validated integer

    Raises:
        ValueError: If value is negative
        TypeError: If value is not an integer
    """
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an integer, got {type(value).__name__}")
    
    if value < 0:
        raise ValueError(f"{name} must be non-negative, got {value}")
    
    return value


def validate_binary_string(binary: str) -> str:
    """
    Validate that string contains only binary digits.

    Args:
        binary: String to validate

    Returns:
        Validated binary string

    Raises:
        ValueError: If string is not valid binary
        TypeError: If input is not a string
    """
    if not isinstance(binary, str):
        raise TypeError(f"Binary input must be a string, got {type(binary).__name__}")
    
    if not binary:
        raise ValueError("Binary string cannot be empty")
    
    if not all(c in '01' for c in binary):
        raise ValueError(f"Invalid binary string: contains non-binary characters")
    
    return binary


def validate_int_list(values: Any, positive_only: bool = False) -> List[int]:
    """
    Validate that values is a list of integers.

    Args:
        values: Values to validate
        positive_only: If True, all values must be positive

    Returns:
        Validated list of integers

    Raises:
        ValueError: If any value is invalid
        TypeError: If values is not a list or contains non-integers
    """
    if not isinstance(values, list):
        raise TypeError(f"Expected list, got {type(values).__name__}")
    
    if not values:
        raise ValueError("List cannot be empty")
    
    for i, value in enumerate(values):
        if not isinstance(value, int):
            raise TypeError(f"Element {i} must be an integer, got {type(value).__name__}")
        
        if positive_only and value <= 0:
            raise ValueError(f"Element {i} must be positive, got {value}")
        elif not positive_only and value < 0:
            raise ValueError(f"Element {i} must be non-negative, got {value}")
    
    return values


def validate_text(text: str, min_length: int = 1) -> str:
    """
    Validate text input.

    Args:
        text: Text to validate
        min_length: Minimum required length

    Returns:
        Validated text

    Raises:
        ValueError: If text is too short
        TypeError: If text is not a string
    """
    if not isinstance(text, str):
        raise TypeError(f"Text must be a string, got {type(text).__name__}")
    
    if len(text) < min_length:
        raise ValueError(f"Text must be at least {min_length} characters, got {len(text)}")
    
    return text