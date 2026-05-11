# -*- coding: utf-8 -*-

from ui.output import CliOutput
from core.file_manager import FileManager
from decoders.registry import REGISTRY


class DefineObfuscation:
    def __init__(
        self,
        file_name: str,
        cli_output: CliOutput,
        file_manager: FileManager,
    ):
        self.output = cli_output
        self.file_manager = file_manager
        self.file_name = file_name

    def detect(self) -> str | None:
        code = self.file_manager.read(self.file_name)

        for info in REGISTRY:
            if info.pattern is None:
                continue

            if info.pattern.search(code):
                return info.key

        return None
