# -*- coding: utf-8 -*-

import os
from typing import Tuple
from core.config import DECODED_FILE_PREFIX
from ui.output import CliOutput

class CliInput:
    def __init__(self, cli_output: CliOutput):
        self.output = cli_output

    def get_function_choice(self) -> str | None:
        while True:
            user_input = input("Your choice: ").strip()
            if user_input == "99":
                return None

            valid_choices = [str(i) for i in range(1, 23)] + ["88"]

            if user_input in valid_choices:
                return user_input
            
            self.output.print_error("Invalid function selection.")
            continue

    def get_file_name(self) -> Tuple[str, str] | None:
        while True:
            file_name = input("Enter file path: ").strip()
            if file_name == "99":
                return None
            
            file_name = file_name + ".py" if not file_name.endswith(".py") else file_name

            if not os.path.exists(file_name):
                self.output.print_error("File does not exist. Enter 99 to exit.")
                continue

            new_base_name = f"{DECODED_FILE_PREFIX}{os.path.basename(file_name)}"
            new_file_name = os.path.join(
                os.path.dirname(file_name), new_base_name
            )

            
            return file_name, new_file_name
