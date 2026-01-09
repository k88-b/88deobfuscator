# -*- coding: utf-8 -*-

import re
from decoders.abstract_decoder import BaseDecodersClass

class XindexObfDeobfuscator(BaseDecodersClass):
    def _decode_string(self, encoded: str) -> str:
        result = []
        for part in encoded.split("|"):
            if len(part) == 10:
                result.append(chr(int(part[5:]) - int(part[:5])))
        return "".join(result)

    def decode(self) -> bool | None:
        try:
            source_pattern = re.compile(
                r"\w+\(\w+\[[0-9]+\]\+\w+\[[0-9]+\]\+\w+\[[0-9]+\]\+\w+\[[0-9]+\]\)"
                r"\s*\(\s*\w+\s*\(\s*[\"']([0-9|]+)[\"']\s*\)\s*\)"
            )
            if not self._match_obfuscation(source_pattern):
                return False

            encoded_string = self.match.group(1)
            self.content = self._decode_string(encoded_string)
            self._write_result()
            
            return True
            
        except Exception as e:
            self.output.print_error(e)
            return None
