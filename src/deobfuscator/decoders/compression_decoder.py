# -*- coding: utf-8 -*-

import ast
import zlib
import gzip
import lzma
from typing import Optional
from core.abstract_decoder import BaseDecodersClass


class CompressionUtilsDecoder(BaseDecodersClass):
    def decode_layer(self, encoded_str: str) -> Optional[str]:
        try:
            bytes_data = ast.literal_eval(f"b'{encoded_str}'")
            module = {"zlib": zlib, "gzip": gzip, "lzma": lzma}[self.algorithm]
            result = module.decompress(bytes_data[::-1])
            return result.decode()

        except Exception as e:
            self.output.print_error(f"Failed to decode the layer: {e}")
            return None

    def decode(self) -> bool:
        try:
            if self.user_choice == "4":
                pattern = self._get_typical_pattern("zlib")
                self.algorithm = "zlib"

            if self.user_choice == "5":
                pattern = self._get_typical_pattern("gzip")
                self.algorithm = "gzip"

            if self.user_choice == "6":
                pattern = self._get_typical_pattern("lzma")
                self.algorithm = "lzma"

            return self.common_decode_logic(
                pattern=pattern,
                clean_pattern=f"_ = lambda __ : __import__('{self.algorithm}').decompress(__[::-1]);",
            )
        except Exception as e:
            self.output.print_error(f"Failed to deobfuscate the file: {e}")
            return False
