"""
Huffman decoding implementation.

Recebe uma string binária e uma tabela de códigos {char: código}.
Inverte a tabela e decodifica bit a bit.
"""

from typing import Dict


def _validate_binary(binary: str) -> str:
    if not isinstance(binary, str):
        raise TypeError("A entrada binária deve ser uma string.")
    binary = binary.replace(" ", "")
    if not binary:
        raise ValueError("A entrada binária não pode estar vazia.")
    if any(bit not in "01" for bit in binary):
        raise ValueError("Código binário inválido — use apenas 0 e 1.")
    return binary


def _validate_codes(codes: Dict[str, str]) -> Dict[str, str]:
    if not isinstance(codes, dict) or not codes:
        raise ValueError("A tabela de códigos não pode estar vazia.")
    for char, code in codes.items():
        if not code or any(b not in "01" for b in code):
            raise ValueError(
                f"Código inválido para '{char}': '{code}' — use apenas 0 e 1."
            )
    # Verifica que nenhum código é prefixo de outro (propriedade prefix-free).
    sorted_codes = sorted(codes.values())
    for i in range(len(sorted_codes) - 1):
        if sorted_codes[i + 1].startswith(sorted_codes[i]):
            raise ValueError(
                f"Tabela de códigos inválida: '{sorted_codes[i]}' é prefixo de "
                f"'{sorted_codes[i + 1]}'. Huffman exige códigos livres de prefixo."
            )
    return codes


def decode(binary: str, codes: Dict[str, str]) -> str:
    """
    Decode Huffman encoded binary string.

    Args:
        binary: Binary string to decode
        codes: Code table mapping characters to their binary codes

    Returns:
        Decoded text string
    """
    binary = _validate_binary(binary)
    codes = _validate_codes(codes)

    # Inverte: código -> caractere
    inv = {code: char for char, code in codes.items()}

    decoded_chars = []
    buffer = ""

    for bit in binary:
        buffer += bit
        if buffer in inv:
            decoded_chars.append(inv[buffer])
            buffer = ""

    if buffer:
        raise ValueError(
            f"Sequência binária inválida: sobrou '{buffer}' sem correspondência."
        )

    result = "".join(decoded_chars)

    print(f"Binário        : {binary}")
    print(f"Tabela usada   : {codes}")
    print(f"Texto decoded  : {result}")

    return result