"""
Elias-Gamma decoding implementation.

Recebe uma string binária e decodifica para uma lista de inteiros.
"""

from typing import List

def _validate_binary(binary: str) -> str:
    if not isinstance(binary, str):
        raise TypeError("A entrada binária deve ser uma string.")
    binary = binary.replace(" ", "")
    if not binary:
        raise ValueError("A entrada binária não pode estar vazia.")
    if any(bit not in "01" for bit in binary):
        raise ValueError("Código binário inválido — use apenas 0 e 1.")
    return binary

def decode(binary: str) -> List[int]:
    """
    Decode Elias-Gamma encoded binary string.

    Args:
        binary: Binary string to decode.

    Returns:
        List of decoded integers.
    """
    binary = _validate_binary(binary)
    result = []
    i = 0
    
    while i < len(binary):
        zeros = 0
        while i < len(binary) and binary[i] == '0':
            zeros += 1
            i += 1
            
        if i + zeros + 1 > len(binary):
            raise ValueError(
                f"Sequência binária inválida: erro ao tentar ler os bits após {zeros} zeros."
            )
            
        bin_part = binary[i : i + zeros + 1]
        result.append(int(bin_part, 2))
        i += zeros + 1

    print(f"Binário         : {binary}")
    print(f"Números decoded : {result}")
    
    return result