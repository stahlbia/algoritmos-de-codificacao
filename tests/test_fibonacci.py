"""
Testes integrados para o módulo Fibonacci (Zeckendorf).
"""

import pytest
from src.encoders.fibonacci import encode, FibonacciResult
from src.decoders.fibonacci_decoder import decode, FibonacciDecodeResult


def flip_bit(binary: str, index: int) -> str:
    bits = list(binary)
    bits[index] = "1" if bits[index] == "0" else "0"
    return "".join(bits)


class TestEncode:
    def test_returns_fibonacci_result(self):
        assert isinstance(encode([5]), FibonacciResult)

    def test_encoded_is_binary_string(self):
        result = encode([1, 10, 15])
        assert all(bit in "01" for bit in result.encoded)

    def test_ends_with_terminator(self):
        assert encode([14]).encoded.endswith("11")

    def test_known_values(self):
        assert encode([1]).encoded == "11"
        assert encode([2]).encoded == "011"
        assert encode([3]).encoded == "0011"
        assert encode([4]).encoded == "1011"
        assert encode([7]).encoded == "01011"

    def test_result_fields(self):
        result = encode([1, 2, 3])
        assert result.numbers == [1, 2, 3]
        assert result.total_bits == len(result.encoded)
        assert result.rate > 0


class TestDecode:
    def test_returns_fibonacci_decode_result(self):
        assert isinstance(decode("11"), FibonacciDecodeResult)

    def test_simple_decode(self):
        assert decode("110110011").numbers == [1, 2, 3]

    def test_decode_result_fields(self):
        result = decode("11")
        assert result.binary == "11"
        assert result.total_bits == 2
        assert result.numbers == [1]

    def test_empty_binary_raises(self):
        with pytest.raises(ValueError):
            decode("")


class TestRoundtripNoError:
    @pytest.mark.parametrize("numbers", [
        [1], [1, 2, 3, 4, 5, 6, 7],
        [10, 20, 30, 40], [100, 500, 1000],
        [8, 13, 21, 34],
    ])
    def test_roundtrip(self, numbers):
        result = encode(numbers)
        assert decode(result.encoded).numbers == numbers


class TestRoundtripWithError:
    def test_single_bit_flip_detected(self):
        numbers = [10, 20, 30]
        result = encode(numbers)
        corrupted = flip_bit(result.encoded, 1)
        assert corrupted != result.encoded
        try:
            assert decode(corrupted).numbers != numbers
        except ValueError:
            pass

    def test_manual_error_indices(self):
        numbers = [7, 14, 21]
        result = encode(numbers)
        corrupted = result.encoded
        for idx in [0, 2, 4]:
            if idx < len(corrupted):
                corrupted = flip_bit(corrupted, idx)
        assert corrupted != result.encoded
        try:
            assert decode(corrupted).numbers != numbers
        except ValueError:
            pass


class TestValidation:
    def test_encode_zero_raises(self):
        with pytest.raises(ValueError):
            encode([0])

    def test_encode_negative_raises(self):
        with pytest.raises(ValueError):
            encode([10, -5, 2])

    def test_encode_non_integer_raises(self):
        with pytest.raises((ValueError, TypeError)):
            encode([1, "fib", 3])
        with pytest.raises((ValueError, TypeError)):
            encode([3.14, 5])