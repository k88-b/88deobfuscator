# -*- coding: utf-8 -*-

# -menu.py config-
BANNER = r"""
╔═════════════════════════╗
║    88 Deobfuscator      ║
╚═════════════════════════╝                                                
"""

FUNCTIONS = """
1  → Base64        7  → B64+Zlib     13 → B64+Lzma
2  → Base32        8  → B32+Zlib     14 → B32+Lzma  
3  → Base16        9  → B16+Zlib     15 → B16+Lzma
4  → Zlib          10 → B64+Gzip     16 → RendyOBF
5  → Gzip          11 → B32+Gzip     17 → Ne4toObf
6  → Lzma          12 → B16+Gzip     18 → BlankOBFv2

19 → ChristianObf  20 → Define Obf
99 → EXIT
"""

# -abstract_decoder.py config-
NOTE = "# Deobfuscated with k88's tool \n# @k88_w\n\n"

EXEC_PATTERN = r"exec\(\(_\)\(b'(.+?)'\)\)"

COMMENTS_PATTERN = r"#(.*?)\n"

TEMP_DIR = ".tempdir"
TEMP_FILE = ".temp.py"
COMPILED_FILE = "__main__.pyc"

# -input.py config-
DECODED_FILE_PREFIX = "decoded_"
