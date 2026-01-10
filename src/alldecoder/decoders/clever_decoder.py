# -*- coding: utf-8 -*-

import re
from core.abstract_decoder import BaseDecodersClass


class CleverObfDeobfuscator(BaseDecodersClass):
    SOURCE_PATTERN = re.compile(
        r"\(\s*lambda\s+__h\s*:\s*\(\s*__h\s*\(\s*\)\s*\)\s*\)\s*"
        r"\(\s*lambda\s*:\s*\(\s*\(\s*_lIlllIllII\s*\[\s*0\s*\]\s*==\s*0\s*\)\s*"
        r"and\s*\(\s*_lIlIlIllII\s*\(\s*0\s*,\s*1\s*\)\s*or\s*_lIllllII\s*"
        r"\(\s*_lIlIIIllII\s*\)\s*\)\s*\)\s*\)",
        re.DOTALL,
    )

    def decode(self) -> bool | None:
        try:
            if not self.pattern_matcher.match_obfuscation(
                self.SOURCE_PATTERN, content=self.content
            ):
                return False

            crack_code = "print(_lIllIlIII)"

            self.content = self.SOURCE_PATTERN.sub(crack_code, self.content)
            self.content = self.code_executor.capture_exec_output(self.content)

            self._write_result()
            return True

        except Exception as e:
            self.output.print_error(e)
            return None
