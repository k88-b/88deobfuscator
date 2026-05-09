# -*- coding: utf-8 -*-

from core.abstract_decoder import BaseDecodersClass


class CleverObfDeobfuscator(BaseDecodersClass):
    def decode(self) -> bool:
        try:
            if not self.pattern_matcher.match_obfuscation(
                self.patterns.CLEVER_OBF_PATTERN, content=self.content
            ):
                return False

            crack_code = "print(_lIllIlIII)"

            self.content = self.patterns.CLEVER_OBF_PATTERN.sub(crack_code, self.content)
            self.content = self.code_executor.capture_exec_output(self.content)

            self._write_result()
            return True

        except Exception as e:
            self.output.print_error(e)
            return False
