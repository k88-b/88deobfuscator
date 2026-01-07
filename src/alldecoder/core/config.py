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
5  → Gzip          11 → B32+Gzip     17 → ChristianObf
6  → Lzma          12 → B16+Gzip     18 → BlankOBFv2

19 → CleverObf     20 → GrandioseeObf
21 → Define Obf
99 → EXIT
"""

# -abstract_decoder.py config-
NOTE = "# Deobfuscated with k88's tool \n# @k88_w\n\n"

EXEC_PATTERN = r"exec\(\(_\)\(b['\"](.+?)['\"]\)\)"

COMMENTS_PATTERN = r"#(.*?)\n"

TEMP_DIR = ".tempdir"
TEMP_FILE = ".temp.py"
COMPILED_FILE = "__main__.pyc"

# -input.py config-
DECODED_FILE_PREFIX = "decoded_"

# -define_obf.py config-
OBFUSCATION_PATTERNS = {
    # base
   	r"_\s*=\s*lambda\s*__\s*:\s*__import__\('base64'\)\.b64decode\(__\[::-1\]\);" : "base64",             
	r"_\s*=\s*lambda\s*__\s*:\s*__import__\('base64'\)\.b32decode\(__\[::-1\]\);" : "base32", 
	r"_\s*=\s*lambda\s*__\s*:\s*__import__\('base64'\)\.b16decode\(__\[::-1\]\);" : "base16",

	# compression
   	r"_\s*=\s*lambda\s*__\s*:\s*__import__\('zlib'\)\.decompress\(__\[::-1\]\);" : "zlib", 
   	r"_\s*=\s*lambda\s*__\s*:\s*__import__\('gzip'\)\.decompress\(__\[::-1\]\);" : "gzip", 
	r"_\s*=\s*lambda\s*__\s*:\s*__import__\('lzma'\)\.decompress\(__\[::-1\]\);" : "lzma",

    # base64 + compression 
   	r"_\s*=\s*lambda\s*__\s*:\s*__import__\('zlib'\)\.decompress\(\s*__import__\('base64'\)\.b64decode\(__\[::-1\]\)\);" : "base64 + zlib",
	r"_\s*=\s*lambda\s*__\s*:\s*__import__\('gzip'\)\.decompress\(\s*__import__\('base64'\)\.b64decode\(__\[::-1\]\)\);" : "base64 + gzip",  
   	r"_\s*=\s*lambda\s*__\s*:\s*__import__\('lzma'\)\.decompress\(\s*__import__\('base64'\)\.b64decode\(__\[::-1\]\)\);" : "base64 + lzma",
   
    # base32 + compression
   	r"_\s*=\s*lambda\s*__\s*:\s*__import__\('zlib'\)\.decompress\(\s*__import__\('base64'\)\.b32decode\(__\[::-1\]\)\);" : "base32 + zlib", 
   	r"_\s*=\s*lambda\s*__\s*:\s*__import__\('gzip'\)\.decompress\(\s*__import__\('base64'\)\.b32decode\(__\[::-1\]\)\);" : "base32 + gzip", 
   	r"_\s*=\s*lambda\s*__\s*:\s*__import__\('lzma'\)\.decompress\(\s*__import__\('base64'\)\.b32decode\(__\[::-1\]\)\);" : "base32 + lzma",

    # base16 + compression
	r"_\s*=\s*lambda\s*__\s*:\s*__import__\('zlib'\)\.decompress\(\s*__import__\('base64'\)\.b16decode\(__\[::-1\]\)\);" : "base16 + zlib", 
   	r"_\s*=\s*lambda\s*__\s*:\s*__import__\('gzip'\)\.decompress\(\s*__import__\('base64'\)\.b16decode\(__\[::-1\]\)\);" : "base16 + gzip", 
	r"_\s*=\s*lambda\s*__\s*:\s*__import__\('lzma'\)\.decompress\(\s*__import__\('base64'\)\.b16decode\(__\[::-1\]\)\);" : "base16 + lzma",

    # marshal
	r"_\s*=\s*lambda\s*__\s*:\s*__import__\('marshal'\)\.loads\(__\[::-1\]\);" : "marshal",

    # marshal + base
   	r"_\s*=\s*lambda\s*__\s*:\s*__import__\('marshal'\)\.loads\(\s*__import__\('base64'\)\.b64decode\(__\[::-1\]\)\);" : "marshal + base64",
   	r"_\s*=\s*lambda\s*__\s*:\s*__import__\('marshal'\)\.loads\(\s*__import__\('base64'\)\.b32decode\(__\[::-1\]\)\);" : "marshal + base32",
   	r"_\s*=\s*lambda\s*__\s*:\s*__import__\('marshal'\)\.loads\(\s*__import__\('base64'\)\.b16decode\(__\[::-1\]\)\);" : "marshal + base16",

    # marshal + compression
	r"_\s*=\s*lambda\s*__\s*:\s*__import__\('marshal'\)\.loads\(__import__\('zlib'\)\.decompress\(__\[::-1\]\)\);" : "marshal + zlib",
	r"_\s*=\s*lambda\s*__\s*:\s*__import__\('marshal'\)\.loads\(__import__\('gzip'\)\.decompress\(__\[::-1\]\)\);" : "marshal + gzip",
	r"_\s*=\s*lambda\s*__\s*:\s*__import__\('marshal'\)\.loads\(__import__\('lzma'\)\.decompress\(__\[::-1\]\)\);" : "marshal + lzma",

    # marshal + compression + base
   	r"_\s*=\s*lambda\s*__\s*:\s*__import__\('marshal'\)\.loads\(__import__\('zlib'\)\.decompress\(\s*__import__\('base64'\)\.b64decode\(__\[::-1\]\)\)\);" : "marshal + zlib + base64",
   	r"_\s*=\s*lambda\s*__\s*:\s*__import__\('marshal'\)\.loads\(__import__\('zlib'\)\.decompress\(\s*__import__\('base64'\)\.b32decode\(__\[::-1\]\)\)\);" : "marshal + zlib + base32",
   	r"_\s*=\s*lambda\s*__\s*:\s*__import__\('marshal'\)\.loads\(__import__\('zlib'\)\.decompress\(\s*__import__\('base64'\)\.b16decode\(__\[::-1\]\)\)\);" : "marshal + zlib + base16",

    # other
   	r"_=lambda __:__import__\('marshal'\)\.loads\(__import__\('gzip'\)\.decompress\(__import__\('lzma'\)\.decompress\(__import__\('zlib'\)\.decompress\(__import__\('base64'\)\.b64decode\(__\[::-1\]\)\)\)\)\);" : "rendy obf (marshal , gzip , lzma , zlib, base64 )"
}

# -christian_obf_decoder.py-
CHRISTIAN_OBF_TEMPLATE_PREFIX= """
def globals():\n    return {'Easy protect by Christian F.': "easy protect by Christian F."}\n__import__('ctypes').pythonapi.PyRun_SimpleString(b'print("Easy protect by Christian F.")')"""
