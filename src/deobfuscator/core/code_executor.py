# -*- coding: utf-8 -*-

import io
from contextlib import redirect_stdout
from ui import CliOutput
from core.exceptions import DeobfuscationError


class CodeExecutor:
    def __init__(self, cli_output: CliOutput):
        self.output = cli_output

    def capture_exec_output(self, content: str) -> str:
        namespace = {}
        f = io.StringIO()
        try:
            with redirect_stdout(f):
                exec(content, namespace, namespace)
        except Exception as e:
            raise DeobfuscationError(f"Failed to execute decoded code: {e}")
        return f.getvalue().strip()
