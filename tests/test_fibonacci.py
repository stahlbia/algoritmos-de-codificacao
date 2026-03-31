"""
Testes integrados para o módulo Fibonacci (Zeckendorf).

Cobre:
  - Codificação baseada no Teorema de Zeckendorf e inserção de terminador
  - Decodificação e recuperação de valores (roundtrip)
  - Inserção manual de erro em bits
  - Verificação de falha/dessincronização na decodificação com erro
  - Casos-limite (números pequenos, formação do terminador '11')
"""

import pytest
from src.encoders.fibonacci import FibonacciEncoder
from src.decoders.fibonacci_decoder import FibonacciDecoder


# ── helpers ───────────────────────────────────────────────────────────

def flip_bit(binary: str, index: int) -> str:
    """Inverte o bit na posição index."""
    bits = list(binary)
    if bits[index] == "0":
        bits[index] = "1"
    else:
        bits[index] = "0"
    return "".join(bits)


# ── Encode ────────────────────────────────────────────────────────────

class TestEncode:
    def test_returns_string(self):
        encoder = FibonacciEncoder()
        result = encoder.encode([5])
        assert isinstance(result, str)

    def test_encoded_is_binary_string(self):
        encoder = FibonacciEncoder()
        encoded = encoder.encode([1, 10, 15])
        assert all(bit in "01" for bit in encoded)

    def test_ends_with_terminator(self):
        encoder = FibonacciEncoder()
        encoded = encoder.encode([14])
        # A representação de Fibonacci sempre termina com '11'
        assert encoded.endswith("11")

    def test_known_values(self):
        encoder = FibonacciEncoder()
        # 1 = Fib(1) -> "1" + "1" = "11"
        assert encoder.encode([1]) == "11"
        # 2 = Fib(2) -> "01" + "1" = "011"
        assert encoder.encode([2]) == "011"
        # 3 = Fib(3) -> "001" + "1" = "0011"
        assert encoder.encode([3]) == "0011"
        # 4 = 1 + 3 -> Fib(1) + Fib(3) -> "101" + "1" = "1011"
        assert encoder.encode([4]) == "1011"
        # 7 = 2 + 5 -> Fib(2) + Fib(4) -> "0101" + "1" = "01011"
        assert encoder.encode([7]) == "01011"


# ── Decode ────────────────────────────────────────────────────────────

class TestDecode:
    def test_simple_decode(self):
        decoder = FibonacciDecoder()
        # "11" -> 1, "011" -> 2, "0011" -> 3
        assert decoder.decode("110110011") == [1, 2, 3]

    def test_empty_binary_returns_empty_list(self):
        decoder = FibonacciDecoder()
        assert decoder.decode("") == []


# ── Roundtrip (encode → decode) SEM erro ──────────────────────────────

class TestRoundtripNoError:
    @pytest.mark.parametrize("numbers", [
        [1],
        [1, 2, 3, 4, 5, 6, 7],
        [10, 20, 30, 40],
        [100, 500, 1000],
        [8, 13, 21, 34], # Próprios números de Fibonacci
    ])
    def test_roundtrip(self, numbers):
        encoder = FibonacciEncoder()
        decoder = FibonacciDecoder()
        
        encoded = encoder.encode(numbers)
        decoded = decoder.decode(encoded)
        assert decoded == numbers


# ── Roundtrip COM inserção de erro em bits ─────────────────────────────

class TestRoundtripWithError:
    def test_single_bit_flip_detected(self):
        encoder = FibonacciEncoder()
        decoder = FibonacciDecoder()
        
        numbers = [10, 20, 30]
        encoded = encoder.encode(numbers)
        corrupted = flip_bit(encoded, 1) # Inverte o segundo bit
        
        assert corrupted != encoded

        try:
            decoded = decoder.decode(corrupted)
            # Inverter um bit em Fibonacci quase sempre muda o valor decodificado
            # ou cria/destrói o terminador '11', dessincronizando o array.
            assert decoded != numbers, (
                "Esperava-se que os números decodificados fossem diferentes após flip de bit.")
        except ValueError:
            pass  

    def test_manual_error_indices(self):
        encoder = FibonacciEncoder()
        decoder = FibonacciDecoder()
        
        numbers = [7, 14, 21]
        encoded = encoder.encode(numbers)
        error_indices = [0, 2, 4]

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
        encoder = FibonacciEncoder()
        with pytest.raises(ValueError):
            encoder.encode([0])

    def test_encode_negative_raises(self):
        encoder = FibonacciEncoder()
        with pytest.raises(ValueError):
            encoder.encode([10, -5, 2])

    def test_encode_non_integer_raises(self):
        encoder = FibonacciEncoder()
        with pytest.raises(ValueError):
            encoder.encode([1, "fib", 3])
        with pytest.raises(ValueError):
            encoder.encode([3.14, 5])