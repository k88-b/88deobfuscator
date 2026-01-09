# -*- coding: utf-8 -*-

import re
from core.abstract_decoder import BaseDecodersClass

class XindexObfDeobfuscator(BaseDecodersClass):
    SOURCE_PATTERN = re.compile(
        r"\w+\(\w+\[[0-9]+\]\+\w+\[[0-9]+\]\+\w+\[[0-9]+\]\+\w+\[[0-9]+\]\)"
        r"\s*\(\s*\w+\s*\(\s*[\"']([0-9|]+)[\"']\s*\)\s*\)"
    )

    def _decode_string(self, encoded: str) -> str:
        result = []
        for part in encoded.split("|"):
            if len(part) == 10:
                result.append(chr(int(part[5:]) - int(part[:5])))
        return "".join(result)

    def decode(self) -> bool | None:
        try:
            self.match = self.pattern_matcher.match_obfuscation(
                self.SOURCE_PATTERN,
                content=self.content,
                return_match=True
            )
            if not self.match:
                return False

            encoded_string = self.match.group(1)
            self.content = self._decode_string(encoded_string)
            self._write_result()
            
            return True
            
        except Exception as e:
            self.output.print_error(e)
            return None
