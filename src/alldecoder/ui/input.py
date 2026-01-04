# -*- coding: utf-8 -*-

import os
from typing import Tuple
from ui.output import CliOutput

class CliInput:
    def __init__(self, cli_output: CliOutput):
        self.output = cli_output

    def get_function_choice(self) -> str:
        while True:
            user_input = input("Ваш выбор: ").strip()
            if user_input == "99":
                print("Выход.")
                raise SystemExit()

            valid_choices = [str(i) for i in range(1, 21)]

            if user_input in valid_choices:
                return user_input
            
            self.output.print_error("Неверный выбор функции.")
            continue

    def get_file_name(self) -> Tuple[str, str]:
        file_name = input("Введите путь до файла: ")
        file_name = file_name + ".py" if not file_name.endswith(".py") else file_name

        if not os.path.exists(file_name):
            self.output.print_error("Файл не существует")
            raise FileNotFoundError()

        new_base_name = f"decoded_{os.path.basename(file_name)}"
        new_file_name = os.path.join(
            os.path.dirname(file_name), new_base_name
        )

            
        return file_name, new_file_name
