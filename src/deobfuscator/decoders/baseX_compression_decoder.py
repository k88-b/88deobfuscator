# -*- coding: utf-8 -*-

import base64
import gzip
import lzma
import zlib
from typing import Optional
from core.abstract_decoder import BaseDecodersClass


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
            self.output.print_error(f"Failed to decode the layer: {e}")
            return None

    def decode(self) -> bool:
        try:
            choices = {
                "7": (
                    self._get_typical_pattern("base64 + zlib"),
                    base64.b64decode,
                    zlib,
                ),
                "8": (
                    self._get_typical_pattern("base32 + zlib"),
                    base64.b32decode,
                    zlib,
                ),
                "9": (
                    self._get_typical_pattern("base16 + zlib"),
                    base64.b16decode,
                    zlib,
                ),
                "10": (
                    self._get_typical_pattern("base64 + gzip"),
                    base64.b64decode,
                    gzip,
                ),
                "11": (
                    self._get_typical_pattern("base32 + gzip"),
                    base64.b32decode,
                    gzip,
                ),
                "12": (
                    self._get_typical_pattern("base16 + gzip"),
                    base64.b16decode,
                    gzip,
                ),
                "13": (
                    self._get_typical_pattern("base64 + lzma"),
                    base64.b64decode,
                    lzma,
                ),
                "14": (
                    self._get_typical_pattern("base32 + lzma"),
                    base64.b32decode,
                    lzma,
                ),
                "15": (
                    self._get_typical_pattern("base16 + lzma"),
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
