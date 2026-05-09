# -*- coding: utf-8 -*-

import ast
import marshal
import gzip
import lzma
import zlib
import base64
from core.abstract_decoder import BaseDecodersClass


class RendyDecoder(BaseDecodersClass):
    def _decode_content(self) -> str:
        encoded = self.match.group(1)
        encoded = ast.literal_eval(f"b'{encoded}'")

        decoded = base64.b64decode(encoded[::-1])
        decoded = zlib.decompress(decoded)
        decoded = lzma.decompress(decoded)
        decoded = gzip.decompress(decoded)
        decoded = marshal.loads(decoded).decode()

        return decoded

    def decode(self) -> bool:
        try:
            self.match = self.pattern_matcher.match_obfuscation(
                self.patterns.RENDY_OBF_PATTERN, content=self.content, return_match=True
            )

            if not self.match:
                return False

            self.content = self._decode_content()

            self.content = self.pattern_matcher.remove_comments(self.content)
            self._write_result()
            return True

        except Exception as e:
            self.output.print_error(f"Failed to deobfuscate the file: {e}")
            return False
