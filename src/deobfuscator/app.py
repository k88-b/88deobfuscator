# -*- coding: utf-8 -*-

import sys
from core.config import AppConfig
from core.patterns import Patterns
from core.file_manager import FileManager
from core.code_executor import CodeExecutor
from core.pattern_matcher import PatternMatcher
from core.exceptions import DeobfuscationError
from ui import CliOutput, CliInput
from ui.menu import Menu
from utils import DefineObfuscation

from decoders.registry import (
    DECODER_REGISTRY,
    MENU_CHOICES,
    get_menu_text,
    get_info_by_choice,
)


class App:
    def __init__(self):
        self.config = AppConfig()
        self.patterns = Patterns()
        self.menu_text = get_menu_text()
        self.valid_choices = set(MENU_CHOICES.keys())
        self.valid_choices.add("88")
        self.output = CliOutput(self.config)
        self.input = CliInput(self.output, self.config)
        self.file_manager = FileManager(self.output, self.config)
        self.code_executor = CodeExecutor(self.output)
        self.pattern_matcher = PatternMatcher(self.output, self.patterns)
        self.menu = Menu(
            cli_output=self.output,
            cli_input=self.input,
            menu_text=self.menu_text,
            valid_choices=self.valid_choices,
            config=self.config,
        )

    def run(self) -> None:
        user_choice, file_name, new_file_name = self.menu.interact()
        if user_choice is None or file_name is None:
            print("Exiting.")
            sys.exit(0)

        if user_choice == "88":
            definer = DefineObfuscation(
                file_name=file_name,
                cli_output=self.output,
                file_manager=self.file_manager,
            )
            method_key = definer.detect()

            if method_key is None:
                print("No obfuscation found.")
                sys.exit(1)

            print(f"Obfuscation found! Name: {method_key}")

            decoder_class = DECODER_REGISTRY[method_key]

        else:
            info = get_info_by_choice(user_choice)
            decoder_class = info.decoder_class
            method_key = info.key

        decoder = decoder_class(
            file_name=file_name,
            new_file_name=new_file_name,
            method_key=method_key,
            cli_output=self.output,
            file_manager=self.file_manager,
            code_executor=self.code_executor,
            pattern_matcher=self.pattern_matcher,
            config=self.config,
            patterns=self.patterns,
        )

        try:
            decoder.decode()

        except DeobfuscationError as e:
            self.output.print_error(str(e))
            sys.exit(1)

        except Exception as e:
            self.output.print_error(f"Failed to deobfuscate file: {e}")
            sys.exit(1)

        print(f"Successfully deobfuscated! Check {new_file_name}")
