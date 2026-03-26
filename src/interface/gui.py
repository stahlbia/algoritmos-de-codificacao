"""
Graphical User Interface for encoding algorithms using customtkinter.

Layout:
  - Left sidebar : 4 algorithm buttons + appearance / scaling controls
  - Center panel : row 0 → title + Golomb-m (same row, title left / m right)
                   row 1 → encode/decode radio buttons
                   row 2 → "Entrada" label
                   row 3 → input textbox  (expands)
                   row 4 → submit button
                   row 5 → "Resultado" label
                   row 6 → output textbox (expands)
                   row 7 → error label
"""

import sys
import tkinter as tk
from io import StringIO

import customtkinter
from src.encoders import golomb, elias_gamma, fibonacci, huffman

# ── default appearance ────────────────────────────────────────────────
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")


class EncoderApp(customtkinter.CTk):
    """Main application window."""

    ALGORITHMS = ["Golomb", "Elias-Gamma", "Fibonacci/Zeckendorf", "Huffman"]

    def __init__(self):
        super().__init__()

        self.title("Algoritmos de Codificação")
        self.geometry("960x620")
        self.minsize(820, 520)

        # ── state variables ──────────────────────────────────────────
        self.selected_algo = tk.StringVar(value=self.ALGORITHMS[0])
        self.operation     = tk.StringVar(value="encode")
        self.golomb_m      = tk.StringVar(value="4")

        # grid: sidebar (col 0) | center (col 1, expands)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_center()

        # highlight first algorithm button
        self._select_algo(self.ALGORITHMS[0])

    # ─────────────────────────── sidebar ─────────────────────────────

    def _build_sidebar(self):
        sb = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        sb.grid(row=0, column=0, sticky="nsew")
        sb.grid_propagate(False)
        sb.grid_rowconfigure(6, weight=1)   # push appearance controls to bottom

        customtkinter.CTkLabel(
            sb,
            text="Algoritmos",
            font=customtkinter.CTkFont(size=18, weight="bold"),
        ).grid(row=0, column=0, padx=20, pady=(24, 14), sticky="w")

        self._algo_buttons: dict[str, customtkinter.CTkButton] = {}
        for i, name in enumerate(self.ALGORITHMS):
            btn = customtkinter.CTkButton(
                sb,
                text=name,
                anchor="w",
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray80", "gray30"),
                command=lambda n=name: self._select_algo(n),
            )
            btn.grid(row=i + 1, column=0, padx=12, pady=4, sticky="ew")
            self._algo_buttons[name] = btn

        # appearance / scaling at bottom
        customtkinter.CTkLabel(sb, text="Aparência:", anchor="w").grid(
            row=7, column=0, padx=20, pady=(10, 0), sticky="w"
        )
        self._appearance_menu = customtkinter.CTkOptionMenu(
            sb,
            values=["Dark", "Light", "System"],
            command=lambda v: customtkinter.set_appearance_mode(v),
        )
        self._appearance_menu.set("Dark")
        self._appearance_menu.grid(row=8, column=0, padx=20, pady=(4, 8), sticky="ew")

        customtkinter.CTkLabel(sb, text="Escala:", anchor="w").grid(
            row=9, column=0, padx=20, pady=(4, 0), sticky="w"
        )
        self._scaling_menu = customtkinter.CTkOptionMenu(
            sb,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self._change_scaling,
        )
        self._scaling_menu.set("100%")
        self._scaling_menu.grid(row=10, column=0, padx=20, pady=(4, 20), sticky="ew")

    # ─────────────────────────── center ──────────────────────────────

    def _build_center(self):
        center = customtkinter.CTkFrame(self, fg_color="transparent")
        center.grid(row=0, column=1, sticky="nsew", padx=30, pady=28)

        # col 0 expands; col 1 is fixed (Golomb m widget)
        center.grid_columnconfigure(0, weight=1)
        center.grid_columnconfigure(1, weight=0)
        # input and output rows expand vertically
        center.grid_rowconfigure(3, weight=2)
        center.grid_rowconfigure(6, weight=3)

        # ── row 0: title (col 0) + Golomb m (col 1) ──────────────────
        self._title_label = customtkinter.CTkLabel(
            center, text="", font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self._title_label.grid(row=0, column=0, sticky="w", pady=(0, 12))

        self._golomb_frame = customtkinter.CTkFrame(center, fg_color="transparent")
        self._golomb_frame.grid(row=0, column=1, sticky="w", padx=(20, 0), pady=(0, 12))
        customtkinter.CTkLabel(
            self._golomb_frame, text="m :", anchor="w"
        ).pack(side="left", padx=(0, 6))
        customtkinter.CTkEntry(
            self._golomb_frame,
            textvariable=self.golomb_m,
            width=64,
            placeholder_text="4",
        ).pack(side="left")
        self._golomb_frame.grid_remove()   # hidden until Golomb is selected

        # ── row 1: encode / decode radio buttons ──────────────────────
        radio_frame = customtkinter.CTkFrame(center, fg_color="transparent")
        radio_frame.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 12))
        self._radio_encode = customtkinter.CTkRadioButton(
            radio_frame,
            text="Codificar",
            variable=self.operation,
            value="encode",
            command=self._on_operation_change,
        )
        self._radio_encode.pack(side="left", padx=(0, 24))
        self._radio_decode = customtkinter.CTkRadioButton(
            radio_frame,
            text="Decodificar",
            variable=self.operation,
            value="decode",
            command=self._on_operation_change,
        )
        self._radio_decode.pack(side="left")

        # ── row 2: input label ─────────────────────────────────────────
        customtkinter.CTkLabel(center, text="Entrada", anchor="w").grid(
            row=2, column=0, columnspan=2, sticky="w"
        )

        # ── row 3: input textbox ───────────────────────────────────────
        self._input_box = customtkinter.CTkTextbox(
            center,
            font=customtkinter.CTkFont(family="Courier", size=14),
            border_spacing=14,
        )
        self._input_box.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(4, 0))

        # ── row 4: submit button ───────────────────────────────────────
        customtkinter.CTkButton(
            center,
            text="▶   Executar",
            font=customtkinter.CTkFont(size=13, weight="bold"),
            command=self._submit,
        ).grid(row=4, column=0, columnspan=2, pady=14, sticky="w")

        # ── row 5: output label ────────────────────────────────────────
        customtkinter.CTkLabel(center, text="Resultado", anchor="w").grid(
            row=5, column=0, columnspan=2, sticky="w"
        )

        # ── row 6: output textbox (read-only) ─────────────────────────
        self._output_box = customtkinter.CTkTextbox(
            center,
            font=customtkinter.CTkFont(family="Courier", size=14),
            border_spacing=14,
            state="disabled",
        )
        self._output_box.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=(4, 0))

        # ── row 7: error label ─────────────────────────────────────────
        self._error_label = customtkinter.CTkLabel(
            center,
            text="",
            text_color="#f38ba8",
            anchor="w",
            wraplength=580,
        )
        self._error_label.grid(row=7, column=0, columnspan=2, sticky="w", pady=(6, 0))

    # ─────────────────────────── helpers ─────────────────────────────

    def _select_algo(self, name: str):
        """Highlight chosen sidebar button and update the title."""
        prev = self.selected_algo.get()
        self.selected_algo.set(name)

        if prev in self._algo_buttons:
            self._algo_buttons[prev].configure(
                fg_color="transparent",
                text_color=("gray10", "gray90"),
            )

        self._algo_buttons[name].configure(
            fg_color=("gray75", "gray25"),
            text_color=("gray10", "gray90"),
        )

        self._title_label.configure(text=name)

        if name == "Golomb":
            self._golomb_frame.grid()
        else:
            self._golomb_frame.grid_remove()

        self._clear_output()
        self._clear_error()

    def _on_operation_change(self):
        """Clear input and output whenever the user switches encode ↔ decode."""
        self._input_box.delete("1.0", "end")
        self._clear_error()

    def _change_scaling(self, value: str):
        customtkinter.set_widget_scaling(int(value.replace("%", "")) / 100)

    # ─────────────────────────── submit ──────────────────────────────

    def _submit(self):
        self._clear_error()
        self._clear_output()

        raw = self._input_box.get("1.0", "end").strip()
        if not raw:
            self._show_error("⚠  A entrada não pode estar vazia.")
            return

        algo = self.selected_algo.get()
        op   = self.operation.get()

        buf        = StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf

        try:
            if op == "encode":
                self._run_encode(algo, raw)
            else:
                self._run_decode(algo, raw)
        except ValueError as exc:
            sys.stdout = old_stdout
            self._show_error(f"⚠  {exc}")
            return
        except Exception as exc:
            sys.stdout = old_stdout
            self._show_error(f"❌  Erro inesperado: {exc}")
            return
        finally:
            sys.stdout = old_stdout

        self._set_output(buf.getvalue())

    # ─────────────── encode / decode dispatch ────────────────────────

    def _run_encode(self, algo: str, raw: str):
        if algo == "Huffman":
            huffman.encode(raw)
        else:
            numbers = self._parse_numbers(raw, allow_zero=(algo == "Golomb"))
            if algo == "Golomb":
                golomb.encode(numbers, m=self._get_m())
            elif algo == "Elias-Gamma":
                elias_gamma.encode(numbers)
            elif algo == "Fibonacci/Zeckendorf":
                fibonacci.encode(numbers)

    def _run_decode(self, algo: str, raw: str):
        if algo == "Huffman":
            parts  = raw.split(None, 1)
            binary = parts[0]
            codes: dict[str, str] = {}
            if len(parts) == 2:
                for pair in parts[1].split():
                    if ":" in pair:
                        ch, code = pair.split(":", 1)
                        codes[ch] = code
            if not codes:
                raise ValueError(
                    "Para decodificar Huffman informe: <binário> <char:código ...>\n"
                    "Exemplo:  10110 a:1 b:01 c:00"
                )
            if not all(c in "01" for c in binary):
                raise ValueError("Código binário inválido — use apenas 0 e 1.")
            huffman.decode(binary, codes)
        else:
            binary = raw.replace(" ", "")
            if not all(c in "01" for c in binary):
                raise ValueError("Código binário inválido — use apenas 0 e 1.")
            if algo == "Golomb":
                golomb.decode(binary, m=self._get_m())
            elif algo == "Elias-Gamma":
                elias_gamma.decode(binary)
            elif algo == "Fibonacci/Zeckendorf":
                fibonacci.decode(binary)

    # ─────────────────────────── utils ───────────────────────────────

    def _get_m(self) -> int:
        try:
            m = int(self.golomb_m.get())
            if m < 1:
                raise ValueError
            return m
        except ValueError:
            raise ValueError("Parâmetro m deve ser um inteiro positivo.")

    @staticmethod
    def _parse_numbers(raw: str, allow_zero: bool = False) -> list[int]:
        try:
            nums = [int(t) for t in raw.split()]
        except ValueError:
            raise ValueError(
                "Entrada inválida — use números inteiros separados por espaço."
            )
        if allow_zero:
            if any(n < 0 for n in nums):
                raise ValueError("Este algoritmo requer números não-negativos (≥ 0).")
        else:
            if any(n <= 0 for n in nums):
                raise ValueError("Este algoritmo requer números positivos (> 0).")
        return nums

    def _set_output(self, text: str):
        self._output_box.configure(state="normal")
        self._output_box.delete("1.0", "end")
        self._output_box.insert("1.0", text)
        self._output_box.configure(state="disabled")

    def _clear_output(self):
        self._output_box.configure(state="normal")
        self._output_box.delete("1.0", "end")
        self._output_box.configure(state="disabled")

    def _show_error(self, msg: str):
        self._error_label.configure(text=msg)

    def _clear_error(self):
        self._error_label.configure(text="")


# ─────────────────────────── entry point ─────────────────────────────

def main():
    app = EncoderApp()
    app.mainloop()


if __name__ == "__main__":
    main()