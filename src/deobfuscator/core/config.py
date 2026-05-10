# -*- coding: utf-8 -*-
from dataclasses import dataclass


@dataclass
class AppConfig:
    NOTE: str = "# Deobfuscated with k88's tool \n# @k88_w\n\n"
    TEMP_DIR: str = ".tempdir"
    TEMP_FILE: str = ".temp.py"
    COMPILED_FILE: str = "__main__.pyc"
    DECODED_FILE_PREFIX: str = "decoded_"
    BANNER: str = r"""
╔═════════════════════════╗
║    88 Deobfuscator      ║
╚═════════════════════════╝                                                
"""
    MENU_COLUMNS = 3
    MENU_SEPARATOR = "    "


default_config = AppConfig()
