# -*- coding: utf-8 -*-

import re
from ui.output import CliOutput
from core.config import OBFUSCATION_PATTERNS
from core.file_manager import FileManager

class DefineObfuscation:
    def __init__(self, file_name: str, cli_output: CliOutput, file_manager: FileManager):
        self.output = cli_output
        self.file_manager = file_manager
        self.file_name = file_name
        
    def define_obfuscation(self) -> None:
        code = self.file_manager.read(self.file_name)
    						
        for key, value  in OBFUSCATION_PATTERNS.items():    
            match = re.search(key, code)

            if match: 
                print(f"Obfuscation found! Name: {value}")
                return
    						
            print("No obfuscation found.")
    								
