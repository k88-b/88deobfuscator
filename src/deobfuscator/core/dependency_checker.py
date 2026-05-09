# -*- coding: utf-8 -*-

import shutil
from ui import CliOutput


class DependencyChecker:
    @staticmethod
    def check_dependencies(output: CliOutput) -> None:
        if shutil.which("pycdc") is None:
            output.print_error(
                "pycdc not found in PATH.\nDownload it from https://github.com/zrax/pycdc\nSome features will be unavailable. (ChristianObf deobfuscator)"
            )
