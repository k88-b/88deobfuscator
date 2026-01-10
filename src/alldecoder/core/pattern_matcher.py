# -*- coding: utf-8 -*-

import re
from typing import Union
from ui import CliOutput
from core.config import AppConfig, default_config


class PatternMatcher:
    def __init__(self, cli_output: CliOutput, config: AppConfig | None = None):
        self.output = cli_output
        self.config = config or default_config

    def match_obfuscation(
        self, pattern: str, content: str, return_match=False
    ) -> Union[bool, re.Match]:
        match = re.search(pattern, content)
        if not match:
            self.output.print_error("Obfuscation not detected.")
            return False

        if return_match:
            return match

        return True

    def remove_comments(self, content: str) -> str:
        try:
            return re.sub(self.config.COMMENTS_PATTERN, "", content, flags=re.DOTALL)

        except Exception as e:
            self.output.print_error(f"Failed to remove comments: {e}")
            return content

    def process_exec_layers(self, content: str, decode_layer_callback) -> str:
        try:
            while re.search(self.config.EXEC_PATTERN, content):
                content = re.sub(
                    self.config.EXEC_PATTERN, decode_layer_callback, content
                )

            return content
        except Exception as e:
            self.output.print_error(f"Failed to process code on one of the layers: {e}")
