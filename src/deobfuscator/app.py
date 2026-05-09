# -*- coding: utf-8 -*-

from decoders import DECODER_REGISTRY
from core.config import AppConfig
from core.patterns import Patterns
from core.file_manager import FileManager
from core.code_executor import CodeExecutor
from core.pattern_matcher import PatternMatcher
from ui import CliOutput, CliInput
from ui.menu import Menu
from utils import DefineObfuscation


class App:
    def __init__(self):
        self.config = AppConfig()
        self.patterns = Patterns()
        self.output = CliOutput(self.config)
        self.input = CliInput(self.output, self.config)
        self.file_manager = FileManager(self.output, self.config)
        self.code_executor = CodeExecutor(self.output)
        self.pattern_matcher = PatternMatcher(self.output, self.patterns)
        self.menu = Menu(
            cli_output=self.output, cli_input=self.input, config=self.config
        )
        self.registry = DECODER_REGISTRY

    def run(self) -> None:
        user_choice, file_name, new_file_name = self.menu.interact()
        if user_choice is None or file_name is None:
            print("Exiting.")
            raise SystemExit()

        if user_choice == "88":
            definer = DefineObfuscation(
                file_name=file_name,
                cli_output=self.output,
                file_manager=self.file_manager,
                patterns=self.patterns,
            )
            definer.define_obfuscation()
            return

        decoder_class = self.registry[user_choice]
        decoder = decoder_class(
            file_name=file_name,
            new_file_name=new_file_name,
            user_choice=user_choice,
            cli_output=self.output,
            file_manager=self.file_manager,
            code_executor=self.code_executor,
            pattern_matcher=self.pattern_matcher,
            config=self.config,
            patterns=self.patterns,
        )
        result = decoder.decode()

        if result:
            print(f"Successfully deobfuscated! Check {new_file_name}")
        else:
            self.output.print_error("Failed to deobfuscate.")
