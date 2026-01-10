# -*- coding: utf-8 -*-

import sys
from core.config import AppConfig, default_config


class CliOutput:
    RED = "\033[1;91m"
    RESET = "\033[0m"

    def __init__(self, config: AppConfig | None = None):
        self.config = config or default_config

    def print_banner(self) -> None:
        # os.system("clear" if os.name == "posix" else "cls")
        print(self.config.BANNER)

    def print_error(self, text: str) -> None:
        print(f"{self.RED}Error! {text}{self.RESET}", file=sys.stderr)
