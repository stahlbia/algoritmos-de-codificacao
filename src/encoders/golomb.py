"""
Golomb encoding implementation.
TODO: implement encoding and decoding logic.
"""

from typing import Union, List


def encode(numbers: Union[int, List[int]], m: int = 4) -> str:
    """
    Encode integer(s) using Golomb coding.

    Args:
        numbers: Single non-negative integer or list of non-negative integers
        m: Golomb parameter (positive integer)

    Returns:
        Binary string representation
    """
    print("[Golomb] encode() chamado")
    print(f"  entrada: {numbers}")
    print(f"  parâmetro m: {m}")
    print("  TODO: implementar codificação Golomb")
    print("  1. Para cada número n, calcular quociente q = n // m e resto r = n % m")
    print("  2. Codificar q em unário (q uns seguidos de um 0)")
    print("  3. Codificar r em binário truncado")
    print("  4. Concatenar unário + binário para cada número")


def decode(binary: str, m: int = 4) -> List[int]:
    """
    Decode Golomb encoded binary string.

    Args:
        binary: Binary string to decode
        m: Golomb parameter (positive integer)

    Returns:
        List of decoded non-negative integers
    """
    print("[Golomb] decode() chamado")
    print(f"  entrada binária: {binary}")
    print(f"  parâmetro m: {m}")
    print("  TODO: implementar decodificação Golomb")
    print("  1. Ler bits em unário para obter o quociente q")
    print("  2. Ler bits em binário truncado para obter o resto r")
    print("  3. Reconstruir número: n = q * m + r")
    print("  4. Repetir até consumir toda a string binária")