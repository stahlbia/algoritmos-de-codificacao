"""
Testes integrados para o módulo Golomb.

Cobre:
  - Codificação de valores individuais e listas
  - Decodificação
  - Roundtrip (encode → decode) sem erro
  - Roundtrip com inserção de erro em bits
  - Diferentes valores de m (1, 2, 4, 8, potência de 2 e não-potência)
  - Validações de entrada
"""

import pytest
from src.encoders.golomb import encode
from src.decoders.golomb_decoder import decode


# ── helpers ───────────────────────────────────────────────────────────

def flip_bit(binary: str, index: int) -> str:
    """Inverte o bit na posição `index` (ignora espaços na contagem)."""
    bits = list(binary)
    bit_idx = 0
    for i, char in enumerate(bits):
        if char in "01":
            if bit_idx == index:
                bits[i] = "1" if char == "0" else "0"
                return "".join(bits)
            bit_idx += 1
    raise IndexError(f"Índice de bit {index} fora do alcance.")


# ── Encode: valores individuais ───────────────────────────────────────

class TestEncodeSingle:
    def test_encode_1_m4(self):
        # n=1 → valor_interno=0 → q=0, r=0 → unário="0", resto="00" → "000"
        assert encode(1, m=4) == "000"

    def test_encode_single_int(self):
        result = encode(5, m=4)
        assert isinstance(result, str)
        assert all(c in "01 " for c in result)

    def test_encode_m1(self):
        # m=1 → unário puro. n=1 → valor=0 → "0"; n=3 → valor=2 → "110"
        assert encode(1, m=1) == "0"
        assert encode(3, m=1) == "110"

    def test_encode_m2(self):
        # m=2 → k=1, c=0. n=1 → val=0 → q=0,r=0 → "00"; n=2 → val=1 → q=0,r=1 → "01"
        assert encode(1, m=2) == "00"
        assert encode(2, m=2) == "01"


# ── Encode: listas ────────────────────────────────────────────────────

class TestEncodeList:
    def test_encode_list(self):
        result = encode([1, 2, 3], m=4)
        parts = result.split()
        assert len(parts) == 3

    def test_encode_list_m1(self):
        result = encode([1, 2, 3], m=1)
        parts = result.split()
        assert parts == ["0", "10", "110"]


# ── Decode ────────────────────────────────────────────────────────────

class TestDecode:
    def test_decode_single(self):
        assert decode("000", m=4) == [1]

    def test_decode_m1(self):
        assert decode("0", m=1) == [1]
        assert decode("110", m=1) == [3]

    def test_decode_m2(self):
        assert decode("00", m=2) == [1]
        assert decode("01", m=2) == [2]

    def test_decode_multiple_concatenated(self):
        # Codifica [1,2,3] com m=4, remove espaços, decodifica
        encoded = encode([1, 2, 3], m=4).replace(" ", "")
        assert decode(encoded, m=4) == [1, 2, 3]


# ── Roundtrip SEM erro ────────────────────────────────────────────────

class TestRoundtripNoError:
    @pytest.mark.parametrize("m", [1, 2, 3, 4, 5, 7, 8, 16])
    def test_roundtrip_single(self, m):
        for n in [1, 2, 3, 5, 10, 20]:
            encoded = encode(n, m=m).replace(" ", "")
            decoded = decode(encoded, m=m)
            assert decoded == [n], f"Falha: n={n}, m={m}"

    @pytest.mark.parametrize("m", [1, 2, 4, 8])
    def test_roundtrip_list(self, m):
        numbers = [1, 3, 5, 7, 10, 15]
        encoded = encode(numbers, m=m).replace(" ", "")
        decoded = decode(encoded, m=m)
        assert decoded == numbers

    def test_roundtrip_large_values(self):
        numbers = [50, 100, 200]
        for m in [4, 7, 16]:
            encoded = encode(numbers, m=m).replace(" ", "")
            decoded = decode(encoded, m=m)
            assert decoded == numbers


# ── Roundtrip COM inserção de erro em bits ─────────────────────────────

class TestRoundtripWithError:
    def test_single_bit_flip(self):
        numbers = [1, 3, 5, 7]
        encoded = encode(numbers, m=4).replace(" ", "")

        corrupted = flip_bit(encoded, 0)
        assert corrupted != encoded

        try:
            decoded = decode(corrupted, m=4)
            assert decoded != numbers, (
                "Esperava-se resultado diferente após flip de bit."
            )
        except ValueError:
            pass  

    def test_multiple_bit_flips(self):
        numbers = [2, 4, 6, 8]
        encoded = encode(numbers, m=4).replace(" ", "")

        corrupted = encoded
        for idx in [0, 2, 4]:
            if idx < len(corrupted.replace(" ", "")):
                corrupted = flip_bit(corrupted, idx)

        try:
            decoded = decode(corrupted, m=4)
            assert decoded != numbers
        except ValueError:
            pass

    def test_manual_error_indices(self):
        numbers = [3, 7, 12]
        encoded = encode(numbers, m=8).replace(" ", "")

        error_indices = [1, 5]
        corrupted = encoded
        for idx in error_indices:
            corrupted = flip_bit(corrupted, idx)

        assert corrupted != encoded

        try:
            decoded = decode(corrupted, m=8)
            assert decoded != numbers
        except ValueError:
            pass


# ── Valores de m não-potência de 2 ────────────────────────────────────

class TestNonPowerOfTwo:
    @pytest.mark.parametrize("m", [3, 5, 6, 7, 9, 10])
    def test_roundtrip_non_power_of_two(self, m):
        numbers = [1, 2, 4, 8, 12]
        encoded = encode(numbers, m=m).replace(" ", "")
        decoded = decode(encoded, m=m)
        assert decoded == numbers


# ── Validações de entrada ──────────────────────────────────────────────

class TestValidation:
    def test_encode_zero_raises(self):
        with pytest.raises(ValueError):
            encode(0, m=4)

    def test_encode_negative_raises(self):
        with pytest.raises(ValueError):
            encode(-1, m=4)

    def test_encode_bool_raises(self):
        with pytest.raises(TypeError):
            encode(True, m=4)

    def test_encode_m_zero_raises(self):
        with pytest.raises(ValueError):
            encode(1, m=0)

    def test_encode_m_negative_raises(self):
        with pytest.raises(ValueError):
            encode(1, m=-1)

    def test_encode_m_bool_raises(self):
        with pytest.raises(ValueError):
            encode(1, m=True)

    def test_encode_empty_list_raises(self):
        with pytest.raises(ValueError):
            encode([], m=4)

    def test_encode_non_int_raises(self):
        with pytest.raises(TypeError):
            encode("abc", m=4)

    def test_decode_empty_raises(self):
        with pytest.raises(ValueError):
            decode("", m=4)

    def test_decode_invalid_binary_raises(self):
        with pytest.raises(ValueError):
            decode("abc", m=4)

    def test_decode_incomplete_raises(self):
        with pytest.raises(ValueError):
            decode("1", m=4)  