# -*- coding: utf-8 -*-

import ast
import zlib
import gzip
import lzma
from typing import Optional
from decoders.abstract_decoder import BaseDecodersClass
 
class CompressionUtilsDecoder(BaseDecodersClass):
    def decode_layer(self, encoded_str: str) -> Optional[str]:
        try:
            bytes_data = ast.literal_eval(f"b'{encoded_str}'")
            module = {"zlib": zlib, "gzip": gzip, "lzma": lzma}[self.algorithm]
            result = module.decompress(bytes_data[::-1])
            return result.decode()

        except Exception as e:
            self.output.print_error(f"Не удалось декодировать слой: {e}")
            return None
        
    def decode(self) -> bool:
        try:            
            if self.user_choice == "4":
                pattern = r"_\s*=\s*lambda\s*__\s*:\s*__import__\('zlib'\)\.decompress\(__\[::-1\]\);exec\(\(_\)\(b'(.*?)'\)\)"
                self.algorithm = "zlib"
            if self.user_choice == "5":
                pattern = r"_\s*=\s*lambda\s*__\s*:\s*__import__\('gzip'\)\.decompress\(__\[::-1\]\);exec\(\(_\)\(b'(.*?)'\)\)"
                self.algorithm = "gzip"
            if self.user_choice == "6":
                pattern = r"_\s*=\s*lambda\s*__\s*:\s*__import__\('lzma'\)\.decompress\(__\[::-1\]\);exec\(\(_\)\(b'(.*?)'\)\)"
                self.algorithm = "lzma"

            return self.common_decode_logic(
                pattern=pattern,
                clean_pattern=f"_ = lambda __ : __import__('{self.algorithm}').decompress(__[::-1]);"
            )
        except Exception as e:
            self.output.print_error(f"Не удалось деобфусцировать файл: {e}")
            return False

