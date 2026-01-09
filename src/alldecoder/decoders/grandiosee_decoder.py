# -*- coding: utf-8 -*-

import re
from core.abstract_decoder import BaseDecodersClass


class GrandioseeObfDeobfuscator(BaseDecodersClass):
    SOURCE_PATTERN = re.compile(
        r"([a-zA-Z0-9_]+\s*\(\s*[a-zA-Z0-9_]+\s*\(\s*[a-zA-Z0-9_]+\s*\)\s*\))\s*"
        r"\(\s*([a-zA-Z0-9_]+\s*\(\s*[a-zA-Z0-9_]+\s*\))\s*\)\s*;\s*"
        r"[a-zA-Z0-9_]+\s*\(\s*[a-zA-Z0-9_]+\s*\(\s*[a-zA-Z0-9_]+\s*\)\s*\)\s*"
        r"\(\s*([a-zA-Z0-9_]+\s*\(\s*[a-zA-Z0-9_]+\s*\))\s*\)\s*;\s*"
        r"([a-zA-Z0-9_]+\s*\(\s*\))"
    )

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
            self.output.print_error(f"First stage decoding error: {e}")
            raise RuntimeError(f"Failed to execute first stage decoding: {e}")

    def _clean_content(self) -> None:
        trash_pattern = r"(print\([^,]*),"
        self.content = re.sub(trash_pattern, r"\1)#", self.content, count=1)

    def decode(self) -> bool | None:
        try:
            self.match = self.pattern_matcher.match_obfuscation(
                self.SOURCE_PATTERN,
                content=self.content,
                return_match=True
            )
            if not self.match:
                return False

            self._extract_components()
            
            self.content = self.content.replace(self.main_obfuscated_block, "")

            decode_logic = self._get_decode_logic()

            self.content += decode_logic + "\n" + self.main_func

            self._clean_content()
            
            self.content = self.code_executor.capture_exec_output(self.content)
            self._write_result()            
            return True
            
        except Exception as e:
            self.output.print_error(e)
            return None
