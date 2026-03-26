from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="algoritmos-codificacao",
    version="0.1.0",
    author="Your Name",
    description="Implementation of encoding algorithms: Golomb, Elias-Gamma, Fibonacci/Zeckendorf, and Huffman",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stahlbia/algoritmos-de-codificacao",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.24.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "encode=src.interface.cli:main",
            "encode-gui=src.interface.gui:main",
        ],
    },
)