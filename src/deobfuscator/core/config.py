# -*- coding: utf-8 -*-
from dataclasses import dataclass, field


@dataclass
class AppConfig:
    NOTE: str = "# Deobfuscated with k88's tool \n# @k88_w\n\n"
    TEMP_DIR: str = ".tempdir"
    TEMP_FILE: str = ".temp.py"
    COMPILED_FILE: str = "__main__.pyc"
    DECODED_FILE_PREFIX: str = "decoded_"
    BANNER: str = r"""
╔═════════════════════════╗
║    88 Deobfuscator      ║
╚═════════════════════════╝                                                
"""
    FUNCTIONS: str = """
1  → Base64        7  → B64+Zlib      13 → B64+Lzma
2  → Base32        8  → B32+Zlib      14 → B32+Lzma  
3  → Base16        9  → B16+Zlib      15 → B16+Lzma
4  → Zlib          10 → B64+Gzip      16 → RendyOBF
5  → Gzip          11 → B32+Gzip      17 → ChristianObf
6  → Lzma          12 → B16+Gzip      18 → BlankOBFv2

19 → CleverObf     20 → GrandioseeObf 21 → XindexObf
22 → ImpostorObf
88 → Define Obf
99 → EXIT
"""


default_config = AppConfig()
