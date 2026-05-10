# -*- coding: utf-8 -*-

from core.abstract_decoder import BaseDecoder
from core.exceptions import DeobfuscationError


class XindexObfDeobfuscator(BaseDecoder):
    def _decode_string(self, encoded: str) -> str:
        result = []
        for part in encoded.split("|"):
            if len(part) == 10:
                result.append(chr(int(part[5:]) - int(part[:5])))
        return "".join(result)

    def decode(self) -> None:
        try:
            self.match = self.pattern_matcher.match_obfuscation(
                self.patterns.XINDEX_OBF_PATTERN, content=self.content
            )

            encoded_string = self.match.group(1)
            self.content = self._decode_string(encoded_string)
            self._write_result()

            return

        except Exception as e:
            raise DeobfuscationError(e)
