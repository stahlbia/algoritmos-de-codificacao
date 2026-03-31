"""
Elias-Gamma encoding implementation.

Recebe uma lista de inteiros positivos e converte para código Elias-Gamma.
"""

from typing import List, Union
from src.decoders.elias_gamma_decoder import decode

def _validate_numbers(numbers: Union[str, List[int]]) -> List[int]:
    if isinstance(numbers, str):
        try:
            numbers = [int(x.strip()) for x in numbers.split() if x.strip()]
        except ValueError:
            raise TypeError("A entrada deve conter apenas números inteiros separados por espaço.")
            
    if not isinstance(numbers, list) or not numbers:
        raise ValueError("A entrada não pode estar vazia.")
        
    for n in numbers:
        if not isinstance(n, int) or n <= 0:
            raise ValueError(f"Valor inválido: '{n}'. Elias-Gamma exige inteiros maiores que zero.")
            
    return numbers

def encode(numbers: Union[str, List[int]]) -> str:
    """
    Encode numbers using Elias-Gamma algorithm.

    Args:
        numbers: String formatada com espaços ou Lista de inteiros a serem codificados.

    Returns:
        Encoded binary string.
    """
    valid_numbers = _validate_numbers(numbers)
    result = []
    
    for n in valid_numbers:
        binary_n = bin(n)[2:] 
        unary_zeros = '0' * (len(binary_n) - 1)
        result.append(unary_zeros + binary_n)
        
    encoded_string = "".join(result)
    
    print(f"Números originais : {valid_numbers}")
    print(f"Binário gerado    : {encoded_string}")
    
    return encoded_string