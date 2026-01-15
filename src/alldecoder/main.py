#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from core.menu import Menu
from core.config import AppConfig
from core.file_manager import FileManager
from core.code_executor import CodeExecutor
from core.pattern_matcher import PatternMatcher
from ui import CliOutput, CliInput


def main():
    config = AppConfig()
    output = CliOutput(config)
    input = CliInput(output, config)
    file_manager = FileManager(output, config)
    code_executor = CodeExecutor(output)
    pattern_matcher = PatternMatcher(output, config)
    menu = Menu(
        cli_output=output,
        cli_input=input,
        file_manager=file_manager,
        pattern_matcher=pattern_matcher,
        code_executor=code_executor,
        config=config,
    )
    menu.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting.")
