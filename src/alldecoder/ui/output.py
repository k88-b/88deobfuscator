# -*- coding: utf-8 -*-

import sys
from core.config import BANNER


class CliOutput:
    RED = "\033[1;91m"
    RESET = "\033[0m"
                    
    def print_banner(self) -> None:
        # os.system("clear" if os.name == "posix" else "cls")
        print(BANNER)

    def print_error(self, text: str) -> None:
        print(f"{self.RED}Error! {text}{self.RESET}", file=sys.stderr)
