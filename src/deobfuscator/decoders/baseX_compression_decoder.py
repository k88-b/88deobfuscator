# -*- coding: utf-8 -*-

import base64
import gzip
import lzma
import zlib
from core.abstract_decoder import BaseDecoder
from core.exceptions import DeobfuscationError


class BaseCompressionUtilsDecoder(BaseDecoder):
    def decode_layer(self, encoded_str: str) -> str:
        try:
            padding = len(encoded_str) % 4
            if padding:
                encoded_str += "=" * (8 - padding)
            decoded = self.special(encoded_str[::-1])
            decompressed = self.algorithm.decompress(decoded)
            return decompressed.decode("utf-8")

        except Exception as e:
            raise DeobfuscationError(f"Failed to decode the layer: {e}")

    def decode(self) -> None:
        try:
            choices = {
                "base64+zlib": (
                    self.patterns.BASE64_ZLIB_PATTERN,
                    base64.b64decode,
                    zlib,
                ),
                "base32+zlib": (
                    self.patterns.BASE32_ZLIB_PATTERN,
                    base64.b32decode,
                    zlib,
                ),
                "base16+zlib": (
                    self.patterns.BASE16_ZLIB_PATTERN,
                    base64.b16decode,
                    zlib,
                ),
                "base64+gzip": (
                    self.patterns.BASE64_GZIP_PATTERN,
                    base64.b64decode,
                    gzip,
                ),
                "base32+gzip": (
                    self.patterns.BASE32_GZIP_PATTERN,
                    base64.b32decode,
                    gzip,
                ),
                "base16+gzip": (
                    self.patterns.BASE16_GZIP_PATTERN,
                    base64.b16decode,
                    gzip,
                ),
                "base64+lzma": (
                    self.patterns.BASE64_LZMA_PATTERN,
                    base64.b64decode,
                    lzma,
                ),
                "base32+lzma": (
                    self.patterns.BASE32_LZMA_PATTERN,
                    base64.b32decode,
                    lzma,
                ),
                "base16+lzma": (
                    self.patterns.BASE16_LZMA_PATTERN,
                    base64.b16decode,
                    lzma,
                ),
            }

            pattern, self.special, self.algorithm = choices[self.method_key]
            self.common_decode_logic(
                pattern=pattern,
                clean_pattern=f"_ = lambda __ : __import__('{self.algorithm.__name__}').decompress(__import__('base64').{self.special.__name__}(__[::-1]));",
            )
            return

        except Exception as e:
            raise DeobfuscationError(e)
