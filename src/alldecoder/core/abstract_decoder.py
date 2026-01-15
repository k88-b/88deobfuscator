# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from ui import CliOutput
from core.config import AppConfig, default_config
from core.file_manager import FileManager
from core.code_executor import CodeExecutor
from core.pattern_matcher import PatternMatcher


class BaseDecodersClass(ABC):
    def __init__(
        self,
        file_name: str,
        new_file_name: str,
        cli_output: CliOutput,
        file_manager: FileManager,
        code_executor: CodeExecutor,
        pattern_matcher: PatternMatcher,
        config: AppConfig | None = None,
        user_choice: str = "",
    ):
        self.config = config or default_config
        self.file_manager = file_manager
        self.code_executor = code_executor
        self.pattern_matcher = pattern_matcher
        self.output = cli_output
        self.file_name = file_name
        self.new_file_name = new_file_name
        self.user_choice = user_choice
        self.content = self._load_content()
        self.temp_file_path = self.file_manager.get_temp_path(self.config.TEMP_FILE)

    def _load_content(self) -> str:
        return self.file_manager.read(self.file_name)

    def _write_result(self) -> None:
        try:
            self.file_manager.write(
                file_name=self.new_file_name,
                content=self.config.NOTE + self.content.strip(),
            )
        except Exception as e:
            self.output.print_error(
                f"Failed to write the final result to the file: {e}"
            )

    def common_decode_logic(self, pattern: str, clean_pattern: str) -> bool:
        if not self.pattern_matcher.match_obfuscation(
            pattern=pattern, content=self.content
        ):
            return False
        self.content = self.pattern_matcher.process_exec_layers(
            content=self.content,
            decode_layer_callback=lambda m: self.decode_layer(m.group(1)),
        )
        self.content = self.content.replace(clean_pattern, "")
        self.content = self.pattern_matcher.remove_comments(self.content)
        self._write_result()
        return True

    @abstractmethod
    def decode(self):
        pass
