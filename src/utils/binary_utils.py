"""
Utility functions for binary operations and conversions.
"""

from typing import Union, List


def binary_to_int(binary: str) -> int:
    """
    Convert binary string to integer.

    Args:
        binary: Binary string

    Returns:
        Integer value

    Raises:
        ValueError: If binary string is invalid
    """
    if not all(c in '01' for c in binary):
        raise ValueError("Invalid binary string")
    return int(binary, 2) if binary else 0


def int_to_binary(n: int, width: int = 0) -> str:
    """
    Convert integer to binary string.

    Args:
        n: Integer to convert
        width: Minimum width (zero-padded), 0 for no padding

    Returns:
        Binary string

    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("Cannot convert negative integer to binary")
    
    binary = bin(n)[2:]  # Remove '0b' prefix
    
    if width > 0:
        binary = binary.zfill(width)
    
    return binary


def binary_to_hex(binary: str) -> str:
    """
    Convert binary string to hexadecimal.

    Args:
        binary: Binary string

    Returns:
        Hexadecimal string

    Raises:
        ValueError: If binary string is invalid
    """
    if not binary:
        return "0"
    
    n = binary_to_int(binary)
    return hex(n)[2:].upper()  # Remove '0x' prefix


def hex_to_binary(hex_str: str) -> str:
    """
    Convert hexadecimal string to binary.

    Args:
        hex_str: Hexadecimal string

    Returns:
        Binary string

    Raises:
        ValueError: If hex string is invalid
    """
    try:
        n = int(hex_str, 16)
        return bin(n)[2:]
    except ValueError:
        raise ValueError("Invalid hexadecimal string")


def format_binary(binary: str, group_size: int = 8, separator: str = ' ') -> str:
    """
    Format binary string with separators for readability.

    Args:
        binary: Binary string
        group_size: Number of bits per group
        separator: Separator string between groups

    Returns:
        Formatted binary string

    Examples:
        >>> format_binary('11010011', 4, ' ')
        '1101 0011'
        >>> format_binary('110100111010', 8, '-')
        '1101-00111010'
    """
    if not binary:
        return binary
    
    groups = []
    for i in range(0, len(binary), group_size):
        groups.append(binary[i:i+group_size])
    
    return separator.join(groups)


def calculate_entropy(text: str) -> float:
    """
    Calculate Shannon entropy of text.

    Args:
        text: Input text

    Returns:
        Entropy value in bits

    Examples:
        >>> calculate_entropy("aaaa")
        0.0
        >>> calculate_entropy("abcd")
        2.0
    """
    if not text:
        return 0.0
    
    from collections import Counter
    import math
    
    freq = Counter(text)
    length = len(text)
    
    entropy = 0.0
    for count in freq.values():
        probability = count / length
        entropy -= probability * math.log2(probability)
    
    return entropy


def hamming_distance(binary1: str, binary2: str) -> int:
    """
    Calculate Hamming distance between two binary strings.

    Args:
        binary1: First binary string
        binary2: Second binary string

    Returns:
        Number of differing bits

    Raises:
        ValueError: If strings have different lengths
    """
    if len(binary1) != len(binary2):
        raise ValueError("Binary strings must have same length")
    
    return sum(b1 != b2 for b1, b2 in zip(binary1, binary2))