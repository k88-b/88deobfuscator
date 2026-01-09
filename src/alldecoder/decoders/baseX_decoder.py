# -*- coding: utf-8 -*-

import base64
from typing import Optional
from core.abstract_decoder import BaseDecodersClass

class BaseDecoder(BaseDecodersClass):
    def decode_layer(self, encoded_str: str) -> Optional[str]:
        try:
            padding = len(encoded_str) % 4
            if padding:
                encoded_str += "=" * (
                    8 - padding
                )

            decoded_str = self.special(encoded_str[::-1])  
            return decoded_str.decode("utf-8")

        except Exception as e:
            self.output.print_error(f"Failed to decode the layer: {e}")
            return None

    def decode(self) -> bool:
        try:
            if self.user_choice == "1":
                pattern = r"_\s*=\s*lambda\s*__\s*:\s*__import__\('base64'\)\.b64decode\(__\[::-1\]\);"
                self.special = base64.b64decode
            elif self.user_choice == "2":
                pattern = r"_\s*=\s*lambda\s*__\s*:\s*__import__\('base64'\)\.b32decode\(__\[::-1\]\);"
                self.special = base64.b32decode
            elif self.user_choice == "3":
                pattern = r"_\s*=\s*lambda\s*__\s*:\s*__import__\('base64'\)\.b16decode\(__\[::-1\]\);"
                self.special = base64.b16decode
                
            return self.common_decode_logic(
                pattern=pattern,
                clean_pattern=f"_ = lambda __ : __import__('base64').{self.special.__name__}(__[::-1]);"            
            )
        except Exception as e:
            self.output.print_error(str(e))
            return False
