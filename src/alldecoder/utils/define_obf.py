# -*- coding: utf-8 -*-

import re
from ui.output import CliOutput


class DefineObfuscation:
    PATTERNS = {
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
    	r"_=lambda __:__import__\('marshal'\)\.loads\(__import__\('gzip'\)\.decompress\(__import__\('lzma'\)\.decompress\(__import__\('zlib'\)\.decompress\(__import__\('base64'\)\.b64decode\(__\[::-1\]\)\)\)\)\);" : "rendy obf (marshal , gzip , lzma , zlib, base64 )",

        }

    def __init__(self, file_name: str, cli_output: CliOutput):
        self.output = cli_output
        self.file_name = file_name
        
    def define_obfuscation(self) -> None:
        with open(self.file_name, "r", encoding = "utf-8") as f:
            code = f.read() 
    						
        for key, value  in self.PATTERNS.items():    
            match = re.search(key, code)

            if match: 
                print(f"Найдена обфускация! Название {value}")
                return
    						
        print("Обфускация не найдена.")
    								
