# -*- coding: utf-8 -*-

import re
from typing import Dict
from dataclasses import dataclass, field


@dataclass
class Patterns:
    EXEC_PATTERN: str = r"exec\(\(_\)\(b['\"](.+?)['\"]\)\)"
    COMMENTS_PATTERN: str = r"#(.*?)\n"

    CHRISTIAN_OBF_LAYER_PATTERN = re.compile(
        r"__import__\('ctypes'\)\.pythonapi\.PyRun_SimpleString"
    )

    CLEVER_OBF_PATTERN = re.compile(
        r"\(\s*lambda\s+__h\s*:\s*\(\s*__h\s*\(\s*\)\s*\)\s*\)\s*"
        r"\(\s*lambda\s*:\s*\(\s*\(\s*_lIlllIllII\s*\[\s*0\s*\]\s*==\s*0\s*\)\s*"
        r"and\s*\(\s*_lIlIlIllII\s*\(\s*0\s*,\s*1\s*\)\s*or\s*_lIllllII\s*"
        r"\(\s*_lIlIIIllII\s*\)\s*\)\s*\)\s*\)",
        re.DOTALL,
    )

    BLANK_OBF_PATTERN = re.compile(
        r"bytes\(\[108,\s?97,\s?118,\s?101\]\[::-1\]\).decode\(\)\)\(bytes\(\[99,\s?101,\s?120,\s?101\]\[::-1\]\)\)"
    )

    BLANK_OBF_FIRST_LAYER_PATTERN = "[99, 101, 120, 101]"

    BLANK_OBF_SECOND_LAYER_PATTERN = "in getattr(__import__(bytes([115, 110, 105, 116, 108, 105, 117, 98][::-1]).decode()), bytes([108, 97, 118, 101][::-1]).decode())(bytes([101, 103, 110, 97, 114][::-1]))"

    BLANK_OBF_THIRD_LAYER_PATTERN = re.compile(
        r"\[\s*('(?:\d{1,3}\.){3}\d{1,3}'\s*,\s*)+"
    )

    BLANK_OBF_THIRD_LAYER_DEOBFUSCATION_PATTERN = re.compile(r"(.*?)\s*=\s*\[.*?\]")

    GRANDIOSEE_OBF_PATTERN = re.compile(
        r"([a-zA-Z0-9_]+\s*\(\s*[a-zA-Z0-9_]+\s*\(\s*[a-zA-Z0-9_]+\s*\)\s*\))\s*"
        r"\(\s*([a-zA-Z0-9_]+\s*\(\s*[a-zA-Z0-9_]+\s*\))\s*\)\s*;\s*"
        r"[a-zA-Z0-9_]+\s*\(\s*[a-zA-Z0-9_]+\s*\(\s*[a-zA-Z0-9_]+\s*\)\s*\)\s*"
        r"\(\s*([a-zA-Z0-9_]+\s*\(\s*[a-zA-Z0-9_]+\s*\))\s*\)\s*;\s*"
        r"([a-zA-Z0-9_]+\s*\(\s*\))"
    )

    GRANDIOSEE_OBF_TRASH_PATTERN = re.compile(r"(print\([^,]*),")

    IMPOSTOR_OBF_PATTERN = re.compile(
        r"(\.b(?:16|64)decode\([^)]+\))"
        r"|(eval\s*\([^)]*chr\([^)]+\))"
        r"|(exec\s*\([^)]*__globals[^)]*\))"
        r"|(Gateway\([^)]*\))"
        r"|(__tunnel\s*\([^)]*->\s*Gateway)"
        r"|(__module_?_?[^=]*=)"
    )

    IMPOSTOR_OBF_ENCODED_DATA_PATTERN = re.compile(r"Interpreter\((b[\"'][^']*[\"'])")

    RENDY_OBF_PATTERN = re.compile(
        r"_=lambda __:__import__\('marshal'\)\.loads\("
        r"__import__\('gzip'\)\.decompress\("
        r"__import__\('lzma'\)\.decompress\("
        r"__import__\('zlib'\)\.decompress\("
        r"__import__\('base64'\)\.b64decode\("
        r"__\[::-1\]\)\)\)\)\);exec\(_\('(.*?)'\)\)"
    )

    XINDEX_OBF_PATTERN = re.compile(
        r"\w+\(\w+\[[0-9]+\]\+\w+\[[0-9]+\]\+\w+\[[0-9]+\]\+\w+\[[0-9]+\]\)"
        r"\s*\(\s*\w+\s*\(\s*[\"']([0-9|]+)[\"']\s*,\s*1\s*\)\s*\)"
    )

    TYPICAL_PATTERNS: Dict[str, str] = field(
        default_factory=lambda: {
            # base
            r"_\s*=\s*lambda\s*__\s*:\s*__import__\('base64'\)\.b64decode\(__\[::-1\]\);": "base64",
            r"_\s*=\s*lambda\s*__\s*:\s*__import__\('base64'\)\.b32decode\(__\[::-1\]\);": "base32",
            r"_\s*=\s*lambda\s*__\s*:\s*__import__\('base64'\)\.b16decode\(__\[::-1\]\);": "base16",
            # compression
            r"_\s*=\s*lambda\s*__\s*:\s*__import__\('zlib'\)\.decompress\(__\[::-1\]\);": "zlib",
            r"_\s*=\s*lambda\s*__\s*:\s*__import__\('gzip'\)\.decompress\(__\[::-1\]\);": "gzip",
            r"_\s*=\s*lambda\s*__\s*:\s*__import__\('lzma'\)\.decompress\(__\[::-1\]\);": "lzma",
            # base64 + compression
            r"_\s*=\s*lambda\s*__\s*:\s*__import__\('zlib'\)\.decompress\(\s*__import__\('base64'\)\.b64decode\(__\[::-1\]\)\);": "base64 + zlib",
            r"_\s*=\s*lambda\s*__\s*:\s*__import__\('gzip'\)\.decompress\(\s*__import__\('base64'\)\.b64decode\(__\[::-1\]\)\);": "base64 + gzip",
            r"_\s*=\s*lambda\s*__\s*:\s*__import__\('lzma'\)\.decompress\(\s*__import__\('base64'\)\.b64decode\(__\[::-1\]\)\);": "base64 + lzma",
            # base32 + compression
            r"_\s*=\s*lambda\s*__\s*:\s*__import__\('zlib'\)\.decompress\(\s*__import__\('base64'\)\.b32decode\(__\[::-1\]\)\);": "base32 + zlib",
            r"_\s*=\s*lambda\s*__\s*:\s*__import__\('gzip'\)\.decompress\(\s*__import__\('base64'\)\.b32decode\(__\[::-1\]\)\);": "base32 + gzip",
            r"_\s*=\s*lambda\s*__\s*:\s*__import__\('lzma'\)\.decompress\(\s*__import__\('base64'\)\.b32decode\(__\[::-1\]\)\);": "base32 + lzma",
            # base16 + compression
            r"_\s*=\s*lambda\s*__\s*:\s*__import__\('zlib'\)\.decompress\(\s*__import__\('base64'\)\.b16decode\(__\[::-1\]\)\);": "base16 + zlib",
            r"_\s*=\s*lambda\s*__\s*:\s*__import__\('gzip'\)\.decompress\(\s*__import__\('base64'\)\.b16decode\(__\[::-1\]\)\);": "base16 + gzip",
            r"_\s*=\s*lambda\s*__\s*:\s*__import__\('lzma'\)\.decompress\(\s*__import__\('base64'\)\.b16decode\(__\[::-1\]\)\);": "base16 + lzma",
            # marshal
            r"_\s*=\s*lambda\s*__\s*:\s*__import__\('marshal'\)\.loads\(__\[::-1\]\);": "marshal",
            # marshal + base
            r"_\s*=\s*lambda\s*__\s*:\s*__import__\('marshal'\)\.loads\(\s*__import__\('base64'\)\.b64decode\(__\[::-1\]\)\);": "marshal + base64",
            r"_\s*=\s*lambda\s*__\s*:\s*__import__\('marshal'\)\.loads\(\s*__import__\('base64'\)\.b32decode\(__\[::-1\]\)\);": "marshal + base32",
            r"_\s*=\s*lambda\s*__\s*:\s*__import__\('marshal'\)\.loads\(\s*__import__\('base64'\)\.b16decode\(__\[::-1\]\)\);": "marshal + base16",
            # marshal + compression
            r"_\s*=\s*lambda\s*__\s*:\s*__import__\('marshal'\)\.loads\(__import__\('zlib'\)\.decompress\(__\[::-1\]\)\);": "marshal + zlib",
            r"_\s*=\s*lambda\s*__\s*:\s*__import__\('marshal'\)\.loads\(__import__\('gzip'\)\.decompress\(__\[::-1\]\)\);": "marshal + gzip",
            r"_\s*=\s*lambda\s*__\s*:\s*__import__\('marshal'\)\.loads\(__import__\('lzma'\)\.decompress\(__\[::-1\]\)\);": "marshal + lzma",
            # marshal + compression + base
            r"_\s*=\s*lambda\s*__\s*:\s*__import__\('marshal'\)\.loads\(__import__\('zlib'\)\.decompress\(\s*__import__\('base64'\)\.b64decode\(__\[::-1\]\)\)\);": "marshal + zlib + base64",
            r"_\s*=\s*lambda\s*__\s*:\s*__import__\('marshal'\)\.loads\(__import__\('zlib'\)\.decompress\(\s*__import__\('base64'\)\.b32decode\(__\[::-1\]\)\)\);": "marshal + zlib + base32",
            r"_\s*=\s*lambda\s*__\s*:\s*__import__\('marshal'\)\.loads\(__import__\('zlib'\)\.decompress\(\s*__import__\('base64'\)\.b16decode\(__\[::-1\]\)\)\);": "marshal + zlib + base16",
            # other
            r"_=lambda __:__import__\('marshal'\)\.loads\(__import__\('gzip'\)\.decompress\(__import__\('lzma'\)\.decompress\(__import__\('zlib'\)\.decompress\(__import__\('base64'\)\.b64decode\(__\[::-1\]\)\)\)\)\);": "rendy obf (marshal , gzip , lzma , zlib, base64 )",
        }
    )

    CHRISTIAN_OBF_TEMPLATE_PREFIX: str = """
def globals():\n    return {'Easy protect by Christian F.': "easy protect by Christian F."}\n__import__('ctypes').pythonapi.PyRun_SimpleString(b'print("Easy protect by Christian F.")')"""
