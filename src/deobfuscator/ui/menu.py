# -*- coding: utf-8 -*-

from typing import Tuple
from core.dependency_checker import DependencyChecker
from core.config import AppConfig, default_config
from ui import CliOutput, CliInput


class Menu:
    def __init__(
        self,
        cli_output: CliOutput,
        cli_input: CliInput,
        menu_text: str,
        valid_choices: set[str] | None = None,
        config: AppConfig | None = None,
    ):
        self.config = config or default_config
        self.output = cli_output
        self.input = cli_input
        self.menu_text = menu_text
        self.valid_choices = valid_choices

    def _show_menu(self) -> None:
        self.output.print_info(self.menu_text)
        DependencyChecker.check_dependencies(self.output)

    def interact(self) -> Tuple[str | None, str | None, str | None]:
        self._show_menu()
        user_choice = self.input.get_function_choice(self.valid_choices)
        if user_choice is None:
            return None, None, None

        file_name, new_file_name = self.input.get_file_name()
        if file_name is None:
            return None, None, None

        return user_choice, file_name, new_file_name
