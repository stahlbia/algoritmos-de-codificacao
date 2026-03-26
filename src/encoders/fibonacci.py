"""
Fibonacci/Zeckendorf encoding implementation.
TODO: implement encoding and decoding logic.
"""

from typing import Union, List


def encode(numbers: Union[int, List[int]]) -> str:
    """
    Encode integer(s) using Fibonacci/Zeckendorf coding.

    Args:
        numbers: Single positive integer or list of positive integers

    Returns:
        Binary string representation with '11' terminators
    """
    print("[Fibonacci/Zeckendorf] encode() chamado")
    print(f"  entrada: {numbers}")
    print("  TODO: implementar codificação Fibonacci/Zeckendorf")
    print("  1. Gerar a sequência de Fibonacci: 1, 2, 3, 5, 8, 13, ...")
    print("  2. Para cada número n, encontrar a representação de Zeckendorf")
    print("     (soma de números de Fibonacci não consecutivos) usando algoritmo guloso")
    print("  3. Representar como string de bits (1 = usa aquele Fibonacci, 0 = não usa)")
    print("  4. Adicionar terminador '11' ao final de cada código")


def decode(binary: str) -> List[int]:
    """
    Decode Fibonacci encoded binary string.

    Args:
        binary: Binary string to decode (with '11' terminators)

    Returns:
        List of decoded positive integers
    """
    print("[Fibonacci/Zeckendorf] decode() chamado")
    print(f"  entrada binária: {binary}")
    print("  TODO: implementar decodificação Fibonacci/Zeckendorf")
    print("  1. Separar os códigos usando o terminador '11'")
    print("  2. Para cada código, somar os números de Fibonacci correspondentes")
    print("     às posições onde o bit é 1")
    print("  3. Repetir até consumir toda a string binária")