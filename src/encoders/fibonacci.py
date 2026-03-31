"""
Fibonacci (Zeckendorf) encoding implementation.

Recebe uma lista de inteiros positivos e converte para código Fibonacci.
"""

from typing import List, Union
from src.decoders.fibonacci_decoder import decode

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
            raise ValueError(f"Valor inválido: '{n}'. Fibonacci exige inteiros maiores que zero.")
            
    return numbers

def encode(numbers: Union[str, List[int]]) -> str:
    """
    Encode numbers using Fibonacci/Zeckendorf algorithm.

    Args:
        numbers: String formatada com espaços ou Lista de inteiros a serem codificados.

    Returns:
        Encoded binary string ending with terminator '11'.
    """
    valid_numbers = _validate_numbers(numbers)
    result = []
    
    for n in valid_numbers:
        fibs = [1, 2]
        while True:
            next_fib = fibs[-1] + fibs[-2]
            if next_fib > n:
                break
            fibs.append(next_fib)
            
        codeword = ['0'] * len(fibs)
        temp = n
        
        for i in range(len(fibs) - 1, -1, -1):
            if fibs[i] <= temp:
                codeword[i] = '1'
                temp -= fibs[i]
                
        codeword.append('1')
        result.append("".join(codeword))
        
    encoded_string = "".join(result)
    
    print(f"Números originais : {valid_numbers}")
    print(f"Binário gerado    : {encoded_string}")
    
    return encoded_string