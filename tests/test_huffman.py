"""
Testes integrados para o módulo Huffman.

Cobre:
  - Entrada textual e construção de árvore/tabela
  - Codificação e decodificação (roundtrip)
  - Inserção manual de erro em bits
  - Verificação de falha na decodificação com erro
  - Casos-limite (1 caractere, texto longo, caracteres especiais)
"""

import pytest
from src.encoders.huffman import (
    build_frequency_table,
    build_tree,
    build_code_table,
    encode,
    HuffmanNode,
)
from src.decoders.huffman_decoder import decode


# ── helpers ───────────────────────────────────────────────────────────

def flip_bit(binary: str, index: int) -> str:
    """Inverte o bit na posição `index`."""
    bits = list(binary)
    if bits[index] == "0":
        bits[index] = "1"
    else:
        bits[index] = "0"
    return "".join(bits)


# ── Tabela de frequências ─────────────────────────────────────────────

class TestFrequencyTable:
    def test_simple(self):
        assert build_frequency_table("aab") == {"a": 2, "b": 1}

    def test_single_char(self):
        assert build_frequency_table("aaaa") == {"a": 4}

    def test_all_unique(self):
        freq = build_frequency_table("abcd")
        assert all(v == 1 for v in freq.values())
        assert len(freq) == 4


# ── Construção da árvore ──────────────────────────────────────────────

class TestBuildTree:
    def test_returns_node(self):
        root = build_tree({"a": 3, "b": 1})
        assert isinstance(root, HuffmanNode)

    def test_root_freq_is_total(self):
        freq = {"a": 5, "b": 3, "c": 2}
        root = build_tree(freq)
        assert root.freq == 10

    def test_single_symbol(self):
        root = build_tree({"x": 7})
        # Deve ter pelo menos um filho.
        assert root.left is not None or root.right is not None


# ── Tabela de códigos ─────────────────────────────────────────────────

class TestCodeTable:
    def test_all_chars_present(self):
        freq = {"a": 5, "b": 3, "c": 2}
        tree = build_tree(freq)
        codes = build_code_table(tree)
        assert set(codes.keys()) == {"a", "b", "c"}

    def test_codes_are_binary_strings(self):
        tree = build_tree({"a": 1, "b": 1, "c": 1})
        codes = build_code_table(tree)
        for code in codes.values():
            assert all(bit in "01" for bit in code)

    def test_prefix_free(self):
        tree = build_tree({"a": 5, "b": 3, "c": 1, "d": 1})
        codes = build_code_table(tree)
        code_list = sorted(codes.values())
        for i in range(len(code_list) - 1):
            assert not code_list[i + 1].startswith(code_list[i])

    def test_single_symbol_gets_code(self):
        tree = build_tree({"z": 10})
        codes = build_code_table(tree)
        assert codes == {"z": "0"}


# ── Encode ────────────────────────────────────────────────────────────

class TestEncode:
    def test_returns_tuple(self):
        result = encode("abc")
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_encoded_is_binary_string(self):
        encoded, _ = encode("hello world")
        assert all(bit in "01" for bit in encoded)

    def test_length_matches(self):
        text = "abracadabra"
        encoded, codes = encode(text)
        expected_len = sum(len(codes[ch]) for ch in text)
        assert len(encoded) == expected_len


# ── Decode ────────────────────────────────────────────────────────────

class TestDecode:
    def test_simple_decode(self):
        codes = {"a": "0", "b": "10", "c": "11"}
        assert decode("01011", codes) == "abc"

    def test_invalid_trailing_bits(self):
        codes = {"a": "0", "b": "10"}
        with pytest.raises(ValueError, match="sobrou"):
            decode("01", codes)  # "01" → 'a' + sobra '1'

    def test_empty_binary_raises(self):
        with pytest.raises(ValueError):
            decode("", {"a": "0"})

    def test_empty_codes_raises(self):
        with pytest.raises(ValueError):
            decode("010", {})


# ── Roundtrip (encode → decode) SEM erro ──────────────────────────────

class TestRoundtripNoError:
    @pytest.mark.parametrize("text", [
        "abracadabra",
        "hello world",
        "aaaaaaa",
        "abcdefghijklmnopqrstuvwxyz",
        "Huffman é legal!",
        "🎉🎉🎉",
        "a",
    ])
    def test_roundtrip(self, text):
        encoded, codes = encode(text)
        decoded = decode(encoded, codes)
        assert decoded == text


# ── Roundtrip COM inserção de erro em bits ─────────────────────────────

class TestRoundtripWithError:
    def test_single_bit_flip_detected(self):
        text = "abracadabra"
        encoded, codes = encode(text)

        corrupted = flip_bit(encoded, 0)
        assert corrupted != encoded

        # A decodificação pode:
        #   (a) retornar texto diferente do original, ou
        #   (b) lançar ValueError se a sequência corrompida for inválida.
        try:
            decoded = decode(corrupted, codes)
            assert decoded != text, (
                "Esperava-se que o texto decodificado fosse diferente após flip de bit.")
        except ValueError:
            pass  

    def test_multiple_bit_flips(self):
        text = "hello world"
        encoded, codes = encode(text)

        corrupted = encoded
        for idx in [0, 2, 4]:
            if idx < len(corrupted):
                corrupted = flip_bit(corrupted, idx)

        try:
            decoded = decode(corrupted, codes)
            assert decoded != text
        except ValueError:
            pass

    def test_manual_error_indices(self):
        """Simula o mecanismo de inserção manual de erro por índices."""
        text = "teste de erro"
        encoded, codes = encode(text)

        error_indices = [1, 3]

        corrupted = encoded
        for idx in error_indices:
            if idx < len(corrupted):
                corrupted = flip_bit(corrupted, idx)

        assert corrupted != encoded

        try:
            decoded = decode(corrupted, codes)
            assert decoded != text
        except ValueError:
            pass


# ── Validações de entrada ──────────────────────────────────────────────

class TestValidation:
    def test_encode_empty_raises(self):
        with pytest.raises(ValueError):
            encode("")

    def test_encode_non_string_raises(self):
        with pytest.raises(TypeError):
            encode(123)

    def test_decode_non_binary_raises(self):
        with pytest.raises(ValueError):
            decode("abc", {"a": "0"})

    def test_decode_prefix_conflict_raises(self):
        with pytest.raises(ValueError, match="prefixo"):
            decode("010", {"a": "0", "b": "01"})