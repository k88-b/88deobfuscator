# -*- coding: utf-8 -*-

import shutil
import os
from ui import CliOutput
from core.config import TEMP_DIR 


class FileManager:
    def __init__(self, cli_output: CliOutput):
        self.output = cli_output
        self.TEMP_DIR = TEMP_DIR

    def get_temp_path(self, filename: str) -> str:
        return os.path.join(self.TEMP_DIR, filename)

    def write(self, file_name: str, content: str) -> bool:
        try:
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(content)
                return True
        except Exception as e:
            self.output.print_error(f"Failed to write content to file {file_name}: {e}")
            return False

    def read(self, file_name: str) -> str:
        try:
            with open(file_name, "r", encoding="utf-8") as f:
                    return f.read()
        except Exception as e:
            self.output.print_error(f"Failed to read the contents of file {file_name}: {e}")
            raise SystemExit()

    def create_temp_dir(self) -> None:
        try:
            os.makedirs(self.TEMP_DIR, exist_ok=True)
        except Exception as e:
            self.output.print_error(f"Failed to create temp directory: {e}")

    def cleanup(self) -> None:
        if os.path.exists(self.TEMP_DIR):
            shutil.rmtree(self.TEMP_DIR)
        else:
            self.output.print_error("Directory .tempdir was not deleted.")


