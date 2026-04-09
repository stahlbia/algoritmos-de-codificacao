"""
Golomb encoding implementation.

Convenção adotada neste projeto:
- a entrada do Golomb deve ser composta por inteiros positivos (> 0),
  conforme o enunciado do trabalho;
- para compatibilizar essa exigência com a formulação do algoritmo,
  codificamos internamente (n - 1);
- portanto:
    valor_interno = n - 1
    q = valor_interno // m
    r = valor_interno % m
"""

from dataclasses import dataclass
from typing import List, Union
import math


@dataclass
class GolombResult:
    numbers: List[int]
    m: int
    encoded_parts: List[str]
    encoded: str
    total_bits: int
    rate: float


def _validate_m(m: int) -> None:
    if not isinstance(m, int) or isinstance(m, bool) or m <= 0:
        raise ValueError("O parâmetro m do Golomb deve ser um inteiro positivo.")


def _normalize_numbers(numbers: Union[int, List[int]]) -> List[int]:
    if isinstance(numbers, int) and not isinstance(numbers, bool):
        numbers = [numbers]
    elif not isinstance(numbers, list):
        raise TypeError("A entrada deve ser um inteiro ou uma lista de inteiros.")

    if not numbers:
        raise ValueError("A entrada não pode ser vazia.")

    normalized = []
    for n in numbers:
        if not isinstance(n, int) or isinstance(n, bool):
            raise TypeError("Todos os valores devem ser inteiros.")
        if n <= 0:
            raise ValueError("O algoritmo Golomb requer números inteiros positivos (> 0).")
        normalized.append(n)

    return normalized


def encode(numbers: Union[int, List[int]], m: int = 4) -> GolombResult:
    """
    Encode positive integer(s) using Golomb coding.

    Args:
        numbers: Single positive integer or list of positive integers
        m: Golomb parameter (positive integer)

    Returns:
        GolombResult dataclass with all encoding information.
    """
    _validate_m(m)
    numbers = _normalize_numbers(numbers)

    k = math.ceil(math.log2(m)) if m > 1 else 0
    c = (2 ** k) - m if m > 1 else 0

    encoded_parts = []

    for n in numbers:
        value = n - 1
        q = value // m
        r = value % m

        unary = "1" * q + "0"

        if m == 1:
            binary = ""
        else:
            if r < c:
                binary = format(r, f"0{k-1}b") if (k - 1) > 0 else ""
            else:
                binary = format(r + c, f"0{k}b")

        encoded_parts.append(unary + binary)

    encoded = " ".join(encoded_parts)
    total_bits = sum(len(p) for p in encoded_parts)
    rate = total_bits / len(numbers)

    return GolombResult(
        numbers=numbers,
        m=m,
        encoded_parts=encoded_parts,
        encoded=encoded,
        total_bits=total_bits,
        rate=rate,
    )


def format_result(result: GolombResult) -> str:
    """Format a GolombResult into a human-readable string."""
    return (
        f"Números originais : {result.numbers}\n"
        f"Parâmetro m       : {result.m}\n"
        f"Binário gerado    : {result.encoded}\n"
        f"Bits totais       : {result.total_bits}\n"
        f"Taxa              : {result.rate:.2f} bits/símbolo"
    )