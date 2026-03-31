# Algoritmos de Codificação

Implementação em Python de algoritmos clássicos de codificação: **Golomb**, **Elias-Gamma**, **Fibonacci/Zeckendorf** e **Huffman**.

## 📋 Descrição

Este projeto fornece implementações completas e testadas de algoritmos de codificação, com **interface gráfica (GUI)** e **linha de comando (CLI)** que permitem:

- ✅ **Interface Gráfica Intuitiva** - Use com cliques, sem comandos
- ✅ Codificar dados usando diferentes algoritmos
- ✅ Decodificar strings binárias de volta aos dados originais
- ✅ Visualizar resultados e estatísticas de compressão
- ✅ Ver árvore de Huffman graficamente
- ✅ Comparar eficiência de diferentes métodos
- ✅ Copiar resultados facilmente

### 🎨 Interfaces Disponíveis

1. **GUI (Graphical User Interface)** - Interface gráfica com tkinter
   - Ideal para iniciantes e uso interativo
   - Visualização clara de resultados
   - Abas separadas para codificação e decodificação

2. **CLI (Command Line Interface)** - Interface de terminal
   - Ideal para automação e uso em scripts
   - Menu interativo no terminal

## 🚀 Instalação

### Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação das Dependências

```bash
# Clone o repositório
git clone https://github.com/stahlbia/algoritmos-de-codificacao.git
cd algoritmos-de-codificacao

# Instale as dependências
pip install -r requirements.txt

# Ou instale em modo desenvolvimento
pip install -e .
```

## 💻 Uso

### Interface Gráfica (GUI)

Execute a interface gráfica:

```bash
python run_gui.py
```

A GUI oferece:

- 🎨 Interface visual intuitiva
- 📊 Visualização de resultados em tempo real
- 📋 Copiar resultados facilmente
- 🌳 Visualização da árvore de Huffman
- 📈 Estatísticas de compressão

### Interface de Linha de Comando (CLI)

Execute a interface de terminal:

```bash
python -m src.interface.cli
```

Ou, se instalado via setup.py:

```bash
encode
```

### Menu Interativo

A CLI apresenta um menu onde você pode:

1. Selecionar o algoritmo de codificação
2. Escolher entre codificar ou decodificar
3. Inserir dados e visualizar resultados

### Exemplos de Uso Programático

#### Golomb

```python
from src.encoders.golomb import GolombEncoder

# Criar encoder com parâmetro m=4
encoder = GolombEncoder(m=4)

# Codificar números
numbers = [0, 5, 10, 15]
encoded = encoder.encode(numbers)
print(f"Codificado: {encoded}")

# Decodificar
decoded = encoder.decode(encoded)
print(f"Decodificado: {decoded}")
```

#### Elias-Gamma

```python
from src.encoders.elias_gamma import EliasGammaEncoder

encoder = EliasGammaEncoder()

# Codificar números positivos
numbers = [1, 5, 10, 17]
encoded = encoder.encode(numbers)
print(f"Codificado: {encoded}")

# Decodificar
decoded = encoder.decode(encoded)
print(f"Decodificado: {decoded}")
```

#### Fibonacci/Zeckendorf

```python
from src.encoders.fibonacci import FibonacciEncoder

encoder = FibonacciEncoder()

# Codificar números positivos
numbers = [1, 3, 7, 15]
encoded = encoder.encode(numbers)
print(f"Codificado: {encoded}")

# Decodificar
decoded = encoder.decode(encoded)
print(f"Decodificado: {decoded}")
```

#### Huffman

```python
from src.encoders.huffman import HuffmanEncoder

encoder = HuffmanEncoder()

# Codificar texto
text = "hello world"
encoded, codes = encoder.encode(text)
print(f"Codificado: {encoded}")
print(f"Tabela de códigos: {codes}")

# Decodificar
decoded = encoder.decode(encoded, codes)
print(f"Decodificado: {decoded}")

# Visualizar árvore
print(encoder.visualize_tree())
```

## 📚 Algoritmos Implementados

### 1. Golomb

**Descrição**: Algoritmo de compressão com parâmetro ajustável `m`. Ideal para distribuições geométricas.

**Características**:

- Parâmetro `m` ajustável
- Codifica números não-negativos
- Divide números em quociente (unário) e resto (binário)

**Complexidade**: O(n) onde n é o valor a codificar

### 2. Elias-Gamma

**Descrição**: Código universal para inteiros positivos. Não requer parâmetros.

**Características**:

- Auto-delimitante
- Eficiente para números pequenos
- Codifica comprimento em unário + valor em binário

**Complexidade**: O(log n)

### 3. Fibonacci/Zeckendorf

**Descrição**: Baseado na representação de Zeckendorf usando números de Fibonacci não-consecutivos.

**Características**:

- Usa terminador '11'
- Representação única para cada número
- Baseado em números de Fibonacci

**Complexidade**: O(log n)

### 4. Huffman

**Descrição**: Algoritmo de compressão baseado em frequência de símbolos.

**Características**:

- Código de comprimento variável
- Ótimo para compressão baseada em frequência
- Constrói árvore binária
- Símbolos mais frequentes têm códigos mais curtos

**Complexidade**: O(n log n) para construção da árvore

## 🗂️ Estrutura do Projeto

``` md
algoritmos-de-codificacao/
├── src/
│   ├── __init__.py
│   ├── encoders/
│   │   ├── __init__.py
│   │   ├── base_encoder.py       # Classe base abstrata
│   │   ├── golomb.py             # Implementação Golomb
│   │   ├── elias_gamma.py        # Implementação Elias-Gamma
│   │   ├── fibonacci.py          # Implementação Fibonacci
│   │   └── huffman.py            # Implementação Huffman
│   ├── decoders/
│   │   ├── elias_gamma_decoder.py      
│   │   ├── fibonacci_decoder.py             
│   │   ├── golomb_decoder.py        
│   │   └── huffman_decoder.py            
│   ├── interface/
│   │   ├── __init__.py
│   │   ├── gui.py 
│   │   └── cli.py                # Interface CLI
│   └── utils/
│       ├── __init__.py
│       ├── binary_utils.py       # Utilitários para binário
│       └── validation.py         # Validação de entrada
├── tests/
│   ├── __init__.py
│   ├── test_golomb.py
│   ├── test_elias_gamma.py
│   ├── test_fibonacci.py
│   └── test_huffman.py
├── requirements.txt
├── setup.py
├── run_gui.py
├── .gitignore
└── README.md
```

## 🧪 Testes

Execute os testes usando pytest:

```bash
# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=src

# Executar testes específicos
pytest tests/test_huffman.py
```

```

## 🛠️ Desenvolvimento

### Configuração do Ambiente

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências de desenvolvimento
pip install -r requirements.txt
pip install -e ".[dev]"
```

### Formatação de Código

```bash
# Formatar código com black
black src/ tests/

# Verificar estilo com flake8
flake8 src/ tests/

# Verificar tipos com mypy
mypy src/
```

## 📊 Comparação de Algoritmos

| Algoritmo | Tipo | Entrada | Parâmetros | Melhor Para |
| --------- | ---- | ------- | ---------- | ----------- |
| **Golomb** | Paramétrico | Não-negativos | m | Distribuições geométricas |
| **Elias-Gamma** | Universal | Positivos | Nenhum | Números pequenos |
| **Fibonacci** | Universal | Positivos | Nenhum | Representação única |
| **Huffman** | Estatístico | Texto/símbolos | Nenhum | Dados com frequências variadas |

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adicionando uma NovaFeature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request


## 📧 Contato

- GitHub: [@stahlbia](https://github.com/stahlbia)
- Repositório: [algoritmos-de-codificacao](https://github.com/stahlbia/algoritmos-de-codificacao)

## 🔗 Referências

- **Golomb Coding**: Solomon W. Golomb (1966)
- **Elias Coding**: Peter Elias (1975)
- **Zeckendorf's Theorem**: Edouard Zeckendorf (1972)
- **Huffman Coding**: David A. Huffman (1952)
