# -*- coding: utf-8 -*-

import re
from typing import Union
from ui import CliOutput
from core.patterns import Patterns
from core.exceptions import DeobfuscationError


class PatternMatcher:
    def __init__(
        self,
        cli_output: CliOutput,
        patterns: Patterns,
    ):
        self.output = cli_output
        self.patterns = patterns

    def match_obfuscation(
        self, pattern: Union[str, re.Pattern], content: str
    ) -> re.Match:
        match = re.search(pattern, content)
        if not match:
            raise DeobfuscationError("Obfuscation not detected.")

        return match

    def remove_comments(self, content: str) -> str:
        try:
            return re.sub(self.patterns.COMMENTS_PATTERN, "", content, flags=re.DOTALL)

        except Exception as e:
            self.output.print_error(f"Failed to remove comments: {e}")
            return content

    def process_exec_layers(self, content: str, decode_layer_callback) -> str:
        try:
            while re.search(self.patterns.EXEC_PATTERN, content):
                content = re.sub(
                    self.patterns.EXEC_PATTERN, decode_layer_callback, content
                )

            return content
        except Exception as e:
            raise DeobfuscationError(
                f"Failed to process code on one of the layers: {e}"
            )
