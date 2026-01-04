# -*- coding: utf-8 -*-

import base64
import gzip
import lzma
import zlib
from typing import Optional
from decoders.abstract_decoder import BaseDecodersClass


class BaseCompressionUtilsDecoder(BaseDecodersClass):
    def decode_layer(self, encoded_str: str) -> Optional[str]:
        try:
            padding = len(encoded_str) % 4
            if padding:
                encoded_str += "=" * (8 - padding)
            decoded = self.special(encoded_str[::-1])
            decompressed = self.algorithm.decompress(decoded)
            return decompressed.decode("utf-8")

        except Exception as e:
            self.output.print_error(f"Не удалось декодировать слой: {e}")
            return None
                
    def decode(self) -> bool:
        try:
            choices = {
                "7": (
                    r"_\s*=\s*lambda\s*__\s*:\s*__import__\('zlib'\)\.decompress\(s*__import__\('base64'\)\.b64decode\(__\[::-1\]\)\);",
                    base64.b64decode,
                    zlib,
                ),
                "8": (
                    r"_\s*=\s*lambda\s*__\s*:\s*__import__\('zlib'\)\.decompress\(s*__import__\('base64'\)\.b32decode\(__\[::-1\]\)\);",
                    base64.b32decode,
                    zlib,
                ),
                "9": (
                    r"_\s*=\s*lambda\s*__\s*:\s*__import__\('zlib'\)\.decompress\(s*__import__\('base64'\)\.b16decode\(__\[::-1\]\)\);",
                    base64.b16decode,
                    zlib,
                ),
                "10": (
                    r"_\s*=\s*lambda\s*__\s*:\s*__import__\('gzip'\)\.decompress\(s*__import__\('base64'\)\.b64decode\(__\[::-1\]\)\);",
                    base64.b64decode,
                    gzip,
                ),
                "11": (
                    r"_\s*=\s*lambda\s*__\s*:\s*__import__\('gzip'\)\.decompress\(s*__import__\('base64'\)\.b32decode\(__\[::-1\]\)\);",
                    base64.b32decode,
                    gzip,
                ),
                "12": (
                    r"_\s*=\s*lambda\s*__\s*:\s*__import__\('gzip'\)\.decompress\(s*__import__\('base64'\)\.b16decode\(__\[::-1\]\)\);",
                    base64.b16decode,
                    gzip,
                ),
                "13": (
                    r"_\s*=\s*lambda\s*__\s*:\s*__import__\('lzma'\)\.decompress\(s*__import__\('base64'\)\.b64decode\(__\[::-1\]\)\);",
                    base64.b64decode,
                    lzma,
                ),
                "14": (
                    r"_\s*=\s*lambda\s*__\s*:\s*__import__\('lzma'\)\.decompress\(s*__import__\('base64'\)\.b32decode\(__\[::-1\]\)\);",
                    base64.b32decode,
                    lzma,
                ),
                "15": (
                    r"_\s*=\s*lambda\s*__\s*:\s*__import__\('lzma'\)\.decompress\(s*__import__\('base64'\)\.b16decode\(__\[::-1\]\)\);",
                    base64.b16decode,
                    lzma,
                ),
            }
            
            pattern, self.special, self.algorithm = choices[self.user_choice]
            return self.common_decode_logic(
                pattern=pattern, 
                clean_pattern=f"_ = lambda __ : __import__('{self.algorithm.__name__}').decompress(__import__('base64').{self.special.__name__}(__[::-1]));",
            )
        except Exception as e:
            self.output.print_error(str(e))
            return False
