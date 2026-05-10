# -*- coding: utf-8 -*-

import base64
from core.abstract_decoder import BaseDecoder
from core.exceptions import DeobfuscationError


class BaseXDecoder(BaseDecoder):
    def decode_layer(self, encoded_str: str) -> str:
        try:
            padding = len(encoded_str) % 4
            if padding:
                encoded_str += "=" * (8 - padding)

            decoded_str = self.special(encoded_str[::-1])
            return decoded_str.decode("utf-8")

        except Exception as e:
            raise DeobfuscationError(f"Failed to decode the layer: {e}")

    def decode(self) -> None:
        try:
            choices = {
                "1": (
                    self._get_typical_pattern("base64"),
                    base64.b64decode,
                ),
                "2": (
                    self._get_typical_pattern("base32"),
                    base64.b32decode,
                ),
                "3": (
                    self._get_typical_pattern("base16"),
                    base64.b16decode,
                ),
            }
            
            pattern, self.special = choices[self.user_choice]

            self.common_decode_logic(
                pattern=pattern,
                clean_pattern=f"_ = lambda __ : __import__('base64').{self.special.__name__}(__[::-1]);",
            )

            return

        except Exception as e:
            raise DeobfuscationError(e)
