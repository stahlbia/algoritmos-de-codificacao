"""
Command-line interface for encoding algorithms.
"""

import sys
from typing import Optional
from src.encoders import golomb, elias_gamma, fibonacci, huffman
from src.decoders import golomb_decoder, elias_gamma_decoder, fibonacci_decoder, huffman_decoder
from src.decoders.golomb_decoder import format_result as golomb_decode_fmt
from src.decoders.elias_gamma_decoder import format_result as elias_decode_fmt
from src.decoders.fibonacci_decoder import format_result as fib_decode_fmt
from src.decoders.huffman_decoder import format_result as huffman_decode_fmt


class EncoderCLI:
    """Command-line interface for encoding algorithms."""

    def __init__(self):
        """Initialize CLI."""
        self.algorithms = {
            '1': 'Golomb',
            '2': 'Elias-Gamma',
            '3': 'Fibonacci/Zeckendorf',
            '4': 'Huffman',
        }
        self.current_algo = None
        self.golomb_m = 4

    def print_header(self):
        """Print application header."""
        print('\n' * 2)
        print("=" * 70)
        print(" " * 15 + "ALGORITMOS DE CODIFICAÇÃO")
        print("=" * 70)
        print()

    def print_menu(self):
        """Print main menu."""
        print("\n" + "─" * 70)
        print("MENU PRINCIPAL")
        print("─" * 70)
        print("1. Golomb")
        print("2. Elias-Gamma")
        print("3. Fibonacci/Zeckendorf")
        print("4. Huffman")
        print("5. Sair")
        print("─" * 70)

    def print_operation_menu(self):
        """Print operation menu."""
        print("\n" + "─" * 70)
        print("OPERAÇÃO")
        print("─" * 70)
        print("1. Codificar (Encode)")
        print("2. Decodificar (Decode)")
        print("3. Voltar ao menu principal")
        print("─" * 70)

    def get_input(self, prompt: str) -> Optional[str]:
        """Get user input."""
        try:
            return input(prompt).strip()
        except KeyboardInterrupt:
            print("\n\n👋 Operação cancelada.")
            return None

    def select_algorithm(self) -> bool:
        """
        Let user select encoding algorithm.

        Returns:
            True if algorithm selected, False to exit
        """
        self.print_menu()
        choice = self.get_input("\nEscolha um algoritmo (1-5): ")

        if choice == '5':
            return False

        if choice not in self.algorithms:
            print("\n❌ Opção inválida!")
            input("\nPressione Enter para continuar...")
            return True

        self.current_algo = self.algorithms[choice]

        if choice == '1':  # Golomb
            m_str = self.get_input("\nInforme o parâmetro m para Golomb (padrão=4): ")
            try:
                self.golomb_m = int(m_str) if m_str else 4
            except ValueError:
                print("\n❌ Valor inválido! Usando m=4")
                self.golomb_m = 4

        print(f"\n✓ Algoritmo selecionado: {self.current_algo}")
        return True

    def encode_operation(self):
        """Handle encoding operation."""
        print(f"\n{'─' * 70}")
        print(f"CODIFICAÇÃO - {self.current_algo}")
        print("─" * 70)

        if self.current_algo == 'Huffman':
            text = self.get_input("\nInforme o texto a codificar: ")
            if not text:
                return
            result = huffman.encode(text)
            print()
            print(huffman.format_result(result))

        else:
            input_str = self.get_input(
                "\nInforme números inteiros separados por espaço: "
            )
            if not input_str:
                return

            try:
                numbers = [int(x) for x in input_str.split()]
            except ValueError:
                print("\n❌ Entrada inválida! Use apenas números inteiros.")
                return

            if self.current_algo == 'Golomb':
                result = golomb.encode(numbers, m=self.golomb_m)
                print()
                print(golomb.format_result(result))
            elif self.current_algo == 'Elias-Gamma':
                result = elias_gamma.encode(numbers)
                print()
                print(elias_gamma.format_result(result))
            elif self.current_algo == 'Fibonacci/Zeckendorf':
                result = fibonacci.encode(numbers)
                print()
                print(fibonacci.format_result(result))

    def decode_operation(self):
        """Handle decoding operation."""
        print(f"\n{'─' * 70}")
        print(f"DECODIFICAÇÃO - {self.current_algo}")
        print("─" * 70)

        binary = self.get_input("\nInforme o código binário: ")
        if not binary:
            return

        if not all(c in '01' for c in binary):
            print("\n❌ Código binário inválido! Use apenas 0 e 1.")
            return

        if self.current_algo == 'Huffman':
            print("\n⚠️  Para Huffman, forneça a tabela de códigos.")
            print("Formato: char:code (separados por espaço)")
            print("Exemplo: a:0 b:10 c:11")

            codes_str = self.get_input("\nTabela de códigos: ")
            if not codes_str:
                return

            codes = {}
            for pair in codes_str.split():
                if ':' in pair:
                    char, code = pair.split(':', 1)
                    codes[char] = code

            result = huffman_decoder.decode(binary, codes)
            print()
            print(huffman_decode_fmt(result))

        elif self.current_algo == 'Golomb':
            result = golomb_decoder.decode(binary, m=self.golomb_m)
            print()
            print(golomb_decode_fmt(result))
        elif self.current_algo == 'Elias-Gamma':
            result = elias_gamma_decoder.decode(binary)
            print()
            print(elias_decode_fmt(result))
        elif self.current_algo == 'Fibonacci/Zeckendorf':
            result = fibonacci_decoder.decode(binary)
            print()
            print(fib_decode_fmt(result))

    def run_operations(self):
        """Run encoding/decoding operations loop."""
        while True:
            self.print_operation_menu()
            choice = self.get_input("\nEscolha uma operação (1-3): ")

            if choice == '3':
                break
            elif choice == '1':
                self.encode_operation()
            elif choice == '2':
                self.decode_operation()
            else:
                print("\n❌ Opção inválida!")

            input("\nPressione Enter para continuar...")

    def run(self):
        """Run the CLI application."""
        try:
            while True:
                self.print_header()

                if not self.select_algorithm():
                    break

                self.run_operations()
                self.current_algo = None

            print("\n👋 Até logo!\n")

        except KeyboardInterrupt:
            print("\n\n👋 Programa encerrado pelo usuário.\n")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}\n")
            sys.exit(1)


def main():
    """Main entry point."""
    cli = EncoderCLI()
    cli.run()


if __name__ == '__main__':
    main()