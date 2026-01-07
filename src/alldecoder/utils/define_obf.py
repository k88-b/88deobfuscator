# -*- coding: utf-8 -*-

import re
from ui.output import CliOutput
from core.config import OBFUSCATION_PATTERNS

class DefineObfuscation:
    def __init__(self, file_name: str, cli_output: CliOutput):
        self.output = cli_output
        self.file_name = file_name
        
    def define_obfuscation(self) -> None:
        with open(self.file_name, "r", encoding = "utf-8") as f:
            code = f.read() 
    						
        for key, value  in OBFUSCATION_PATTERNS.items():    
            match = re.search(key, code)

            if match: 
                print(f"Obfuscation found! Name: {value}")
                return
    						
            print("No obfuscation found.")
    								
