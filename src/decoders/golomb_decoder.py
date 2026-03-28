"""
Golomb decoding implementation.

Convenção adotada neste projeto:
- o código Golomb representa inteiros positivos (> 0);
- internamente a codificação foi feita sobre (n - 1);
- portanto, ao decodificar:
    valor_interno = q * m + r
    n = valor_interno + 1
"""

import math
from typing import List


def _validate_m(m: int) -> None:
    if not isinstance(m, int) or isinstance(m, bool) or m <= 0:
        raise ValueError("O parâmetro m do Golomb deve ser um inteiro positivo.")


def _validate_binary(binary: str) -> str:
    if not isinstance(binary, str):
        raise TypeError("A entrada binária deve ser uma string.")

    binary = binary.replace(" ", "")

    if not binary:
        raise ValueError("A entrada binária não pode estar vazia.")

    if any(bit not in "01" for bit in binary):
        raise ValueError("Código binário inválido — use apenas 0 e 1.")

    return binary


def decode(binary: str, m: int = 4) -> List[int]:
    """
    Decode Golomb encoded binary string.

    Args:
        binary: Binary string to decode
        m: Golomb parameter (positive integer)

    Returns:
        List of decoded positive integers
    """
    _validate_m(m)
    binary = _validate_binary(binary)

    k = math.ceil(math.log2(m)) if m > 1 else 0
    c = (2 ** k) - m if m > 1 else 0

    decoded_numbers = []
    i = 0

    while i < len(binary):
        # Lê a parte unária: sequência de 1s até encontrar 0.
        q = 0
        while i < len(binary) and binary[i] == "1":
            q += 1
            i += 1

        if i >= len(binary):
            raise ValueError("Sequência binária inválida (falta bit de parada do unário).")

        # Consome o zero final do unário.
        i += 1

        # Caso especial: m = 1 => não há parte do resto.
        if m == 1:
            r = 0
        else:
            prefix_len = k - 1

            if i + prefix_len > len(binary):
                raise ValueError("Sequência binária inválida (resto incompleto).")

            x_str = binary[i:i + prefix_len]
            x = int(x_str, 2) if prefix_len > 0 else 0
            i += prefix_len

            if x < c:
                r = x
            else:
                if i >= len(binary):
                    raise ValueError(
                        "Sequência binária inválida (falta bit adicional do resto)."
                    )
                x = (x << 1) | int(binary[i])
                i += 1
                r = x - c

        value = q * m + r

        # Como o encoder codifica (n - 1), aqui voltamos para n.
        n = value + 1
        decoded_numbers.append(n)

    return decoded_numbers