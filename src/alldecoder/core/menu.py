# -*- coding: utf-8 -*-

import shutil
from ui import CliOutput, CliInput
from decoders import (
    BaseDecoder,
    CompressionUtilsDecoder,
    BaseCompressionUtilsDecoder,
    BlankObfDeobfuscator,
    RendyDecoder,
    Ne4toObfDeobfuscator,
    ChristianObfDeobfuscator
)
from utils import DefineObfuscation
from core.config import FUNCTIONS


class DependencyChecker:
    @staticmethod
    def check_dependencies(output: CliOutput) -> None:
        if shutil.which("pycdc") is None:
            output.print_error(
                "pycdc не найден в PATH\nСкачать https://github.com/zrax/pycdc\nНекоторые функции не будут работать. (Ne4toObf deobfuscator, ChristianObf deobfuscator)"
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
        "17": Ne4toObfDeobfuscator,
        "18": BlankObfDeobfuscator,
        "19": ChristianObfDeobfuscator,
        "20": DefineObfuscation
    }

    def __init__(self):
        self.output = CliOutput()
        self.input = CliInput(self.output) 

    def _show_menu(self) -> None:
        self.output.print_banner()
        DependencyChecker.check_dependencies(self.output)
        print(FUNCTIONS)

    def _check_user_input(self, value: str | None) -> None:
        if value is None:
            print("Выход.")
            raise SystemExit()

    def _process_user_choice(self, user_choice: str, file_name: str, new_file_name: str) -> None:
        if user_choice == "20":
            definer = DefineObfuscation(
                file_name=file_name,
                cli_output=self.output
            )
            definer.define_obfuscation() 
            return
            
        decoder_class = self.DECODER_MAP[user_choice]
        decoder = decoder_class(
            file_name=file_name,
            new_file_name=new_file_name,
            user_choice=user_choice,
            cli_output=self.output
        )
        result = decoder.decode()
        if result:
            print(f"Успешно деобфусцировано! Проверьте {new_file_name}")
        else:
            self.output.print_error("Не удалось деобфусцировать.")
    
    def run(self) -> None:
        self._show_menu()

        user_choice = self.input.get_function_choice()
        self._check_user_input(user_choice)
        
        file_data = self.input.get_file_name()
        self._check_user_input(file_data)

        file_name, new_file_name = file_data
            
        self._process_user_choice(
            user_choice=user_choice,
            file_name=file_name,
            new_file_name=new_file_name
        )
        

