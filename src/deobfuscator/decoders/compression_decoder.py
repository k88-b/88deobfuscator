# -*- coding: utf-8 -*-

import ast
import zlib
import gzip
import lzma
from core.abstract_decoder import BaseDecoder
from core.exceptions import DeobfuscationError


class CompressionUtilsDecoder(BaseDecoder):
    def decode_layer(self, encoded_str: str) -> str:
        try:
            bytes_data = ast.literal_eval(f"b'{encoded_str}'")
            module = {"zlib": zlib, "gzip": gzip, "lzma": lzma}[self.algorithm]
            result = module.decompress(bytes_data[::-1])
            return result.decode()

        except Exception as e:
            raise DeobfuscationError(f"Failed to decode the layer: {e}")

    def decode(self) -> None:
        try:
            choices = {
                "4": (
                    self._get_typical_pattern("zlib"),
                    "zlib",
                ),
                "5": (
                    self._get_typical_pattern("gzip"),
                    "gzip",
                ),
                "6": (
                    self._get_typical_pattern("lzma"),
                    "lzma",
                ),
            }
            
            pattern, self.algorithm = choices[self.user_choice]
                

            self.common_decode_logic(
                pattern=pattern,
                clean_pattern=f"_ = lambda __ : __import__('{self.algorithm}').decompress(__[::-1]);",
            )

            return

        except Exception as e:
            raise DeobfuscationError(f"Failed to deobfuscate the file: {e}")
