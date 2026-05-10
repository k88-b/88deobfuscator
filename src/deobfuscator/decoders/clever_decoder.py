# -*- coding: utf-8 -*-

from core.abstract_decoder import BaseDecoder
from core.exceptions import DeobfuscationError


class CleverObfDeobfuscator(BaseDecoder):
    def decode(self) -> None:
        try:
            self.pattern_matcher.match_obfuscation(
                self.patterns.CLEVER_OBF_PATTERN, content=self.content
            )

            crack_code = "print(_lIllIlIII)"

            self.content = self.patterns.CLEVER_OBF_PATTERN.sub(
                crack_code, self.content
            )
            self.content = self.code_executor.capture_exec_output(self.content)

            self._write_result()
            return

        except Exception as e:
            raise DeobfuscationError(e)
