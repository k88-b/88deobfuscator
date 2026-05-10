# -*- coding: utf-8 -*-

from core.abstract_decoder import BaseDecoder
from core.exceptions import DeobfuscationError


class GrandioseeObfDeobfuscator(BaseDecoder):
    def _extract_components(self):
        self.main_obfuscated_block = self.match.group(0)
        self.exec_wrapper = self.match.group(1)
        self.arg_0 = self.match.group(2)
        self.arg_1 = self.match.group(3)
        self.main_func = self.match.group(4)

    def _get_decode_logic(self) -> str:
        try:
            temp_content = self.content + f"print({self.arg_0});print({self.arg_1})"
            output = self.code_executor.capture_exec_output(temp_content)
            output = output.replace(self.exec_wrapper, "print")
            return output
        except Exception as e:
            raise DeobfuscationError(f"Failed to execute first stage decoding: {e}")

    def _clean_content(self) -> None:
        self.content = self.patterns.GRANDIOSEE_OBF_TRASH_PATTERN.sub(
            r"\1)#", self.content, count=1
        )

    def decode(self) -> None:
        try:
            self.match = self.pattern_matcher.match_obfuscation(
                self.patterns.GRANDIOSEE_OBF_PATTERN, content=self.content
            )

            self._extract_components()

            self.content = self.content.replace(self.main_obfuscated_block, "")

            decode_logic = self._get_decode_logic()

            self.content += decode_logic + "\n" + self.main_func

            self._clean_content()

            self.content = self.code_executor.capture_exec_output(self.content)
            self._write_result()
            return

        except Exception as e:
            raise DeobfuscationError(e)
