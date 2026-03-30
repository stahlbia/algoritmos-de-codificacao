"""
Huffman encoding implementation.

Fluxo:
  1. Calcular frequência de cada caractere do texto
  2. Construir a árvore de Huffman (min-heap)
  3. Gerar a tabela de códigos (percorrer árvore)
  4. Codificar o texto usando a tabela
"""

import heapq
from collections import Counter
from typing import Dict, List, Optional, Tuple


class HuffmanNode:
    """Nó da árvore de Huffman."""

    def __init__(self, char: Optional[str], freq: int,
                 left: Optional["HuffmanNode"] = None,
                 right: Optional["HuffmanNode"] = None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other: "HuffmanNode") -> bool:
        return self.freq < other.freq


def _validate_text(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("A entrada deve ser uma string.")
    if not text:
        raise ValueError("O texto não pode estar vazio.")
    return text


def build_frequency_table(text: str) -> Dict[str, int]:
    """Retorna dicionário {caractere: frequência}."""
    return dict(Counter(text))


def build_tree(freq_table: Dict[str, int]) -> HuffmanNode:
    """
    Constrói a árvore de Huffman a partir da tabela de frequências.

    Retorna o nó raiz.
    """
    if not freq_table:
        raise ValueError("Tabela de frequências vazia.")

    heap: List[HuffmanNode] = [
        HuffmanNode(char=ch, freq=f) for ch, f in freq_table.items()
    ]
    heapq.heapify(heap)

    if len(heap) == 1:
        node = heapq.heappop(heap)
        return HuffmanNode(char=None, freq=node.freq, left=node, right=None)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(
            char=None,
            freq=left.freq + right.freq,
            left=left,
            right=right,
        )
        heapq.heappush(heap, merged)

    return heap[0]


def build_code_table(root: HuffmanNode) -> Dict[str, str]:
    """
    Percorre a árvore e gera {caractere: código_binário}.
    Esquerda = '0', Direita = '1'.
    """
    codes: Dict[str, str] = {}

    def _traverse(node: Optional[HuffmanNode], prefix: str) -> None:
        if node is None:
            return
        if node.char is not None:
            codes[node.char] = prefix if prefix else "0"
            return
        _traverse(node.left, prefix + "0")
        _traverse(node.right, prefix + "1")

    _traverse(root, "")
    return codes


def encode(text: str) -> Tuple[str, Dict[str, str]]:
    """
    Encode text using Huffman coding.

    Args:
        text: Text string to encode

    Returns:
        Tuple of (encoded binary string, code table dictionary)
    """
    text = _validate_text(text)

    freq_table = build_frequency_table(text)
    tree = build_tree(freq_table)
    code_table = build_code_table(tree)

    encoded = "".join(code_table[ch] for ch in text)

    print(f"Texto original : {text}")
    print(f"Frequências    : {freq_table}")
    print(f"Tabela de codes: {code_table}")
    print(f"Binário        : {encoded}")
    print(f"Bits totais    : {len(encoded)}")
    print(f"Taxa           : {len(encoded) / len(text):.2f} bits/símbolo")

    return encoded, code_table