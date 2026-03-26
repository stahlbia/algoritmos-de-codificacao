"""
Huffman encoding implementation.
TODO: implement encoding and decoding logic.
"""

from typing import Dict, Optional, Tuple


def encode(text: str) -> Tuple[str, Dict[str, str]]:
    """
    Encode text using Huffman coding.

    Args:
        text: Text string to encode

    Returns:
        Tuple of (encoded binary string, code table dictionary)
    """
    print("[Huffman] encode() chamado")
    print(f"  entrada: '{text}'")
    print("  TODO: implementar codificação Huffman")
    print("  1. Calcular a frequência de cada símbolo no texto")
    print("  2. Criar um nó folha para cada símbolo")
    print("  3. Construir a árvore de Huffman usando uma fila de prioridade (min-heap):")
    print("     - Retirar os dois nós de menor frequência")
    print("     - Criar um nó interno com a soma das frequências")
    print("     - Repetir até restar um único nó (raiz)")
    print("  4. Gerar os códigos percorrendo a árvore (esquerda=0, direita=1)")
    print("  5. Codificar o texto substituindo cada símbolo pelo seu código")


def decode(binary: str, codes: Dict[str, str]) -> str:
    """
    Decode Huffman encoded binary string.

    Args:
        binary: Binary string to decode
        codes: Code table mapping characters to their binary codes

    Returns:
        Decoded text string
    """
    print("[Huffman] decode() chamado")
    print(f"  entrada binária: {binary}")
    print(f"  tabela de códigos: {codes}")
    print("  TODO: implementar decodificação Huffman")
    print("  1. Inverter a tabela de códigos (código -> símbolo)")
    print("  2. Percorrer a string binária bit a bit, acumulando bits")
    print("  3. Quando o acumulado coincidir com um código, emitir o símbolo")
    print("  4. Repetir até consumir toda a string binária")