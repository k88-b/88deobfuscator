# -*- coding: utf-8 -*-

import io
import subprocess
from contextlib import redirect_stdout
from ui import CliOutput


class CodeExecutor:
    def __init__(self, cli_output: CliOutput):
        self.output = cli_output

    def capture_exec_output(self, content: str) -> str:
        namespace = {}
        f = io.StringIO()
        with redirect_stdout(f):
            exec(content, namespace, namespace)
        return f.getvalue().strip()

    def redirect_python_output(self, source_file: str, output_file: str) -> bool:
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                subprocess.run(["python3", source_file], stdout=f, text=True)
                return True
        except Exception as e:
            self.output.print_error(
                f"Failed to redirect output from the temporary file: {e}"
            )
            return False
