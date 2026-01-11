# -*- coding: utf-8 -*-

import shutil
from ui import CliOutput, CliInput
from decoders import (
    BaseDecoder,
    CompressionUtilsDecoder,
    BaseCompressionUtilsDecoder,
    BlankObfDeobfuscator,
    RendyDecoder,
    ChristianObfDeobfuscator,
    CleverObfDeobfuscator,
    GrandioseeObfDeobfuscator,
    XindexObfDeobfuscator,
    ImpostorObfDeobfuscator,
)
from utils import DefineObfuscation
from core.config import AppConfig, default_config
from core.file_manager import FileManager
from core.code_executor import CodeExecutor
from core.pattern_matcher import PatternMatcher


class DependencyChecker:
    @staticmethod
    def check_dependencies(output: CliOutput) -> None:
        if shutil.which("pycdc") is None:
            output.print_error(
                "pycdc not found in PATH.\nDownload it from https://github.com/zrax/pycdc\nSome features will be unavailable. (ChristianObf deobfuscator)"
            )


class Menu:
    DECODER_MAP = {
        "1": BaseDecoder,
        "2": BaseDecoder,
        "3": BaseDecoder,
        "4": CompressionUtilsDecoder,
        "5": CompressionUtilsDecoder,
        "6": CompressionUtilsDecoder,
        "7": BaseCompressionUtilsDecoder,
        "8": BaseCompressionUtilsDecoder,
        "9": BaseCompressionUtilsDecoder,
        "10": BaseCompressionUtilsDecoder,
        "11": BaseCompressionUtilsDecoder,
        "12": BaseCompressionUtilsDecoder,
        "13": BaseCompressionUtilsDecoder,
        "14": BaseCompressionUtilsDecoder,
        "15": BaseCompressionUtilsDecoder,
        "16": RendyDecoder,
        "17": ChristianObfDeobfuscator,
        "18": BlankObfDeobfuscator,
        "19": CleverObfDeobfuscator,
        "20": GrandioseeObfDeobfuscator,
        "21": XindexObfDeobfuscator,
        "22": ImpostorObfDeobfuscator,
        "88": DefineObfuscation,
    }

    def __init__(
        self,
        cli_output: CliOutput,
        cli_input: CliInput,
        file_manager: FileManager,
        pattern_matcher: PatternMatcher,
        code_executor: CodeExecutor,
        config: AppConfig | None = None    
    ):
        self.config = config or default_config
        self.output = cli_output
        self.input = cli_input
        self.file_manager = file_manager
        self.code_executor = code_executor
        self.pattern_matcher = pattern_matcher

    def _show_menu(self) -> None:
        self.output.print_banner()
        DependencyChecker.check_dependencies(self.output)
        print(self.config.FUNCTIONS)

    def _check_user_input(self, value: str | None) -> None:
        if value is None:
            print("Выход.")
            raise SystemExit()

    def _process_user_choice(
        self, user_choice: str, file_name: str, new_file_name: str
    ) -> None:
        if user_choice == "88":
            definer = DefineObfuscation(
                file_name=file_name,
                cli_output=self.output,
                file_manager=self.file_manager,
                config=self.config,
            )
            definer.define_obfuscation()
            return

        decoder_class = self.DECODER_MAP[user_choice]
        decoder = decoder_class(
            file_name=file_name,
            new_file_name=new_file_name,
            user_choice=user_choice,
            cli_output=self.output,
            file_manager=self.file_manager,
            code_executor=self.code_executor,
            pattern_matcher=self.pattern_matcher,
            config=self.config,
        )
        result = decoder.decode()
        if result:
            print(f"Successfully deobfuscated! Check {new_file_name}")
        else:
            self.output.print_error("Failed to deobfuscate.")

    def run(self) -> None:
        self._show_menu()

        user_choice = self.input.get_function_choice()
        self._check_user_input(user_choice)

        file_data = self.input.get_file_name()
        self._check_user_input(file_data)

        file_name, new_file_name = file_data

        self._process_user_choice(
            user_choice=user_choice, file_name=file_name, new_file_name=new_file_name
        )
