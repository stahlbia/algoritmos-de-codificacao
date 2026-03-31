"""
Fibonacci (Zeckendorf) decoding implementation.

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
    Decode Fibonacci encoded binary string.

    Args:
        binary: Binary string to decode.

    Returns:
        List of decoded integers.
    """
    binary = _validate_binary(binary)
    fibs = [1, 2]
    result = []
    i = 0
    
    while i < len(binary):
        n = 0
        fib_idx = 0
        last_bit = '0'
        terminator_found = False
        
        while i < len(binary):
            bit = binary[i]
            i += 1
            
            if bit == '1' and last_bit == '1':
                terminator_found = True
                break
                
            if bit == '1':
                while len(fibs) <= fib_idx:
                    fibs.append(fibs[-1] + fibs[-2])
                n += fibs[fib_idx]
                
            last_bit = bit
            fib_idx += 1
            
        if not terminator_found:
            raise ValueError("Sequência binária inválida: terminador '11' não encontrado no final.")
            
        result.append(n)

    print(f"Binário         : {binary}")
    print(f"Números decoded : {result}")
    
    return result