# Guia Rápido - Algoritmos de Codificação

## 🚀 Início Rápido

### 1. Instalação

```bash
# Clone o repositório
git clone https://github.com/stahlbia/algoritmos-de-codificacao.git
cd algoritmos-de-codificacao

# Instale as dependências
pip install -r requirements.txt
```

### 2. Interface Gráfica (Recomendado)

A maneira mais fácil de usar o projeto:

```bash
python run_gui.py
```

**Recursos da GUI:**

- ✨ Interface visual intuitiva
- 🔄 Alternância fácil entre algoritmos
- 📊 Visualização de estatísticas
- 🌳 Árvore de Huffman visual
- 📋 Copiar resultados com um clique

### 3. Interface de Linha de Comando

Para usar no terminal:

```bash
python -m src.interface.cli
```

### 4. Uso Programático

```python
from src.encoders.huffman import HuffmanEncoder

encoder = HuffmanEncoder()
encoded, codes = encoder.encode("hello world")
decoded = encoder.decode(encoded, codes)
print(decoded)  # "hello world"
```

## 📚 Algoritmos Disponíveis

| Algoritmo | Entrada | Uso Ideal |
| --------- | ------- | --------- |
| **Golomb** | Números ≥ 0 | Distribuições geométricas |
| **Elias-Gamma** | Números > 0 | Números pequenos |
| **Fibonacci** | Números > 0 | Representação única |
| **Huffman** | Texto | Compressão de texto |

## 💡 Exemplos

### Codificar Números (GUI)

1. Selecione o algoritmo (ex: Golomb)
2. Configure parâmetros se necessário (m=4)
3. Digite números: `0 5 10 15`
4. Clique em "Codificar"
5. Veja o resultado binário e estatísticas

### Codificar Texto (GUI)

1. Selecione "Huffman"
2. Digite seu texto: `hello world`
3. Clique em "Codificar"
4. Veja a tabela de códigos e árvore

### Decodificar (GUI)

1. Vá para aba "Decodificar"
2. Cole o código binário
3. Para Huffman, forneça a tabela de códigos
4. Clique em "Decodificar"

## 🧪 Testar Instalação

```bash
# Executar testes rápidos
python run_examples.py

# Executar demo da GUI
python examples/gui_demo.py

# Executar exemplos
python examples/encode_example.py
```

## ❓ Problemas Comuns

### Erro ao importar tkinter

**macOS:**

``` bash
brew install python-tk
```

**Ubuntu/Debian:**

``` bash
sudo apt-get install python3-tk
```

**Windows:**
Tkinter já vem incluído com Python.

### Erro de módulo não encontrado

``` bash
# Certifique-se de estar no diretório correto
cd algoritmos-de-codificacao

# Reinstale dependências
pip install -r requirements.txt
```

## 📖 Mais Informações

- Leia [README.md](README.md) para documentação completa
- Veja [examples/](examples/) para mais exemplos
- Execute testes com `pytest tests/`

## 🎯 Próximos Passos

1. ✅ Execute `python run_gui.py` para experimentar
2. ✅ Teste diferentes algoritmos com seus dados
3. ✅ Compare taxas de compressão
4. ✅ Explore os exemplos em `examples/`

---

**Dica:** A interface gráfica é a maneira mais fácil de começar! 🚀
