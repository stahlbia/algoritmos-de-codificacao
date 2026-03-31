"""
Testes integrados para o módulo Elias-Gamma.

Cobre:
  - Codificação de inteiros positivos e geração de prefixos unários
  - Decodificação e recuperação de valores (roundtrip)
  - Inserção manual de erro em bits
  - Verificação de falha/dessincronização na decodificação com erro
  - Casos-limite (números pequenos, números grandes) e validações (N <= 0)
"""

import pytest
from src.encoders.elias_gamma import EliasGammaEncoder
from src.decoders.elias_gamma_decoder import EliasGammaDecoder


# ── helpers ───────────────────────────────────────────────────────────

def flip_bit(binary: str, index: int) -> str:
    """Inverte o bit na posição `index`."""
    bits = list(binary)
    if bits[index] == "0":
        bits[index] = "1"
    else:
        bits[index] = "0"
    return "".join(bits)


# ── Encode ────────────────────────────────────────────────────────────

class TestEncode:
    def test_returns_string(self):
        encoder = EliasGammaEncoder()
        result = encoder.encode([5])
        assert isinstance(result, str)

    def test_encoded_is_binary_string(self):
        encoder = EliasGammaEncoder()
        encoded = encoder.encode([1, 10, 15])
        assert all(bit in "01" for bit in encoded)

    def test_known_values(self):
        encoder = EliasGammaEncoder()
        # 1 em binário é '1'. Tamanho 1. Zero zeros = "1"
        assert encoder.encode([1]) == "1"
        # 2 em binário é '10'. Tamanho 2. Um zero = "010"
        assert encoder.encode([2]) == "010"
        # 5 em binário é '101'. Tamanho 3. Dois zeros = "00101"
        assert encoder.encode([5]) == "00101"
        # 9 em binário é '1001'. Tamanho 4. Três zeros = "0001001"
        assert encoder.encode([9]) == "0001001"


# ── Decode ────────────────────────────────────────────────────────────

class TestDecode:
    def test_simple_decode(self):
        decoder = EliasGammaDecoder()
        # "1" -> 1, "010" -> 2, "00101" -> 5
        assert decoder.decode("101000101") == [1, 2, 5]

    def test_invalid_trailing_bits(self):
        decoder = EliasGammaDecoder()
        # "001" -> Indica 2 zeros (tamanho 3), mas só tem 3 bits no total (precisaria de 5)
        with pytest.raises(ValueError, match="malformada"):
            decoder.decode("001")

    def test_empty_binary_returns_empty_list(self):
        decoder = EliasGammaDecoder()
        assert decoder.decode("") == []


# ── Roundtrip (encode → decode) SEM erro ──────────────────────────────

class TestRoundtripNoError:
    @pytest.mark.parametrize("numbers", [
        [1],
        [1, 2, 3, 4, 5],
        [10, 20, 50, 100],
        [255, 256, 1024, 2048],
        [7, 14, 21, 28, 35],
    ])
    def test_roundtrip(self, numbers):
        encoder = EliasGammaEncoder()
        decoder = EliasGammaDecoder()
        
        encoded = encoder.encode(numbers)
        decoded = decoder.decode(encoded)
        assert decoded == numbers


# ── Roundtrip COM inserção de erro em bits ─────────────────────────────

class TestRoundtripWithError:
    def test_single_bit_flip_detected(self):
        encoder = EliasGammaEncoder()
        decoder = EliasGammaDecoder()
        
        numbers = [10, 20, 30]
        encoded = encoder.encode(numbers)
        corrupted = flip_bit(encoded, 0)
        
        assert corrupted != encoded

        try:
            decoded = decoder.decode(corrupted)
            assert decoded != numbers, (
                "Esperava-se que os números decodificados fossem diferentes após flip de bit.")
        except ValueError:
            pass  

    def test_manual_error_indices(self):
        encoder = EliasGammaEncoder()
        decoder = EliasGammaDecoder()
        
        numbers = [5, 15, 25]
        encoded = encoder.encode(numbers)
        error_indices = [1, 3]

        corrupted = encoded
        for idx in error_indices:
            if idx < len(corrupted):
                corrupted = flip_bit(corrupted, idx)

        assert corrupted != encoded

        try:
            decoded = decoder.decode(corrupted)
            assert decoded != numbers
        except ValueError:
            pass


# ── Validações de entrada ──────────────────────────────────────────────

class TestValidation:
    def test_encode_zero_raises(self):
        encoder = EliasGammaEncoder()
        with pytest.raises(ValueError):
            encoder.encode([0])

    def test_encode_negative_raises(self):
        encoder = EliasGammaEncoder()
        with pytest.raises(ValueError):
            encoder.encode([5, -2, 10])

    def test_encode_non_integer_raises(self):
        encoder = EliasGammaEncoder()
        with pytest.raises(ValueError):
            encoder.encode([1, "dois", 3])
        with pytest.raises(ValueError):
            encoder.encode([1.5, 2])