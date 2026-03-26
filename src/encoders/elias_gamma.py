"""
Elias-Gamma encoding implementation.
TODO: implement encoding and decoding logic.
"""

from typing import Union, List


def encode(numbers: Union[int, List[int]]) -> str:
    """
    Encode integer(s) using Elias-Gamma coding.

    Args:
        numbers: Single positive integer or list of positive integers

    Returns:
        Binary string representation
    """
    print("[Elias-Gamma] encode() chamado")
    print(f"  entrada: {numbers}")
    print("  TODO: implementar codificação Elias-Gamma")
    print("  1. Para cada número n, obter sua representação binária")
    print("  2. Calcular k = floor(log2(n)) (número de bits - 1)")
    print("  3. Prefixar com k zeros seguidos de um 1 (ou k uns seguidos de um 0)")
    print("  4. Concatenar prefixo unário + representação binária completa de n")


def decode(binary: str) -> List[int]:
    """
    Decode Elias-Gamma encoded binary string.

    Args:
        binary: Binary string to decode

    Returns:
        List of decoded positive integers
    """
    print("[Elias-Gamma] decode() chamado")
    print(f"  entrada binária: {binary}")
    print("  TODO: implementar decodificação Elias-Gamma")
    print("  1. Contar os uns iniciais para obter k (comprimento - 1)")
    print("  2. Pular o zero separador")
    print("  3. Ler os próximos k+1 bits como número binário")
    print("  4. Repetir até consumir toda a string binária")