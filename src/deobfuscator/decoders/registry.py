# -*- coding: utf-8 -*-

import re
from dataclasses import dataclass
from typing import Type
from itertools import zip_longest

from core.config import AppConfig
from core.patterns import Patterns
from core.abstract_decoder import BaseDecoder
from .baseX_decoder import BaseXDecoder
from .compression_decoder import CompressionUtilsDecoder
from .baseX_compression_decoder import BaseCompressionUtilsDecoder
from .blank_decoder import BlankObfDeobfuscator
from .rendy_decoder import RendyDecoder
from .christian_decoder import ChristianObfDeobfuscator
from .clever_decoder import CleverObfDeobfuscator
from .grandiosee_decoder import GrandioseeObfDeobfuscator
from .xindex_decoder import XindexObfDeobfuscator
from .impostor_decoder import ImpostorObfDeobfuscator

config = AppConfig()


@dataclass(frozen=True)
class ObfuscationInfo:
    key: str
    pattern: re.Pattern | None
    decoder_class: Type[BaseDecoder]


REGISTRY = [
    ObfuscationInfo("base64", Patterns.BASE64_PATTERN, BaseXDecoder),
    ObfuscationInfo("base32", Patterns.BASE32_PATTERN, BaseXDecoder),
    ObfuscationInfo("base16", Patterns.BASE16_PATTERN, BaseXDecoder),
    ObfuscationInfo("zlib", Patterns.ZLIB_PATTERN, CompressionUtilsDecoder),
    ObfuscationInfo("gzip", Patterns.GZIP_PATTERN, CompressionUtilsDecoder),
    ObfuscationInfo("lzma", Patterns.LZMA_PATTERN, CompressionUtilsDecoder),
    ObfuscationInfo(
        "base64+zlib", Patterns.BASE64_ZLIB_PATTERN, BaseCompressionUtilsDecoder
    ),
    ObfuscationInfo(
        "base64+gzip", Patterns.BASE64_GZIP_PATTERN, BaseCompressionUtilsDecoder
    ),
    ObfuscationInfo(
        "base64+lzma", Patterns.BASE64_LZMA_PATTERN, BaseCompressionUtilsDecoder
    ),
    ObfuscationInfo(
        "base32+zlib", Patterns.BASE32_ZLIB_PATTERN, BaseCompressionUtilsDecoder
    ),
    ObfuscationInfo(
        "base32+gzip", Patterns.BASE32_GZIP_PATTERN, BaseCompressionUtilsDecoder
    ),
    ObfuscationInfo(
        "base32+lzma", Patterns.BASE32_LZMA_PATTERN, BaseCompressionUtilsDecoder
    ),
    ObfuscationInfo(
        "base16+zlib", Patterns.BASE16_ZLIB_PATTERN, BaseCompressionUtilsDecoder
    ),
    ObfuscationInfo(
        "base16+gzip", Patterns.BASE16_GZIP_PATTERN, BaseCompressionUtilsDecoder
    ),
    ObfuscationInfo(
        "base16+lzma", Patterns.BASE16_LZMA_PATTERN, BaseCompressionUtilsDecoder
    ),
    ObfuscationInfo("rendy", Patterns.RENDY_OBF_PATTERN, RendyDecoder),
    ObfuscationInfo("christian", None, ChristianObfDeobfuscator),
    ObfuscationInfo("blank", Patterns.BLANK_OBF_PATTERN, BlankObfDeobfuscator),
    ObfuscationInfo("clever", Patterns.CLEVER_OBF_PATTERN, CleverObfDeobfuscator),
    ObfuscationInfo(
        "grandiosee", Patterns.GRANDIOSEE_OBF_PATTERN, GrandioseeObfDeobfuscator
    ),
    ObfuscationInfo("xindex", Patterns.XINDEX_OBF_PATTERN, XindexObfDeobfuscator),
    ObfuscationInfo("impostor", Patterns.IMPOSTOR_OBF_PATTERN, ImpostorObfDeobfuscator),
]


DECODER_REGISTRY = {info.key: info.decoder_class for info in REGISTRY}

MENU_CHOICES = {str(i): info for i, info in enumerate(REGISTRY, 1)}


def format_key_for_menu(key: str) -> str:
    parts = key.split("+")
    formatted_parts = [p.capitalize() for p in parts]
    return " + ".join(formatted_parts)


def get_menu_text() -> str:
    items = [
        f"{num:>2} → {format_key_for_menu(info.key)}"
        for num, info in enumerate(REGISTRY, 1)
    ]
    col_widths = [0] * config.MENU_COLUMNS
    for i, item in enumerate(items):
        col_idx = i % config.MENU_COLUMNS
        col_widths[col_idx] = max(col_widths[col_idx], len(item))

    lines = []
    for chunk in zip_longest(*[iter(items)] * config.MENU_COLUMNS, fillvalue=""):
        line_parts = []
        for col, item in enumerate(chunk):
            if item:
                line_parts.append(item.ljust(col_widths[col]))
            else:
                line_parts.append("")
        lines.append(config.MENU_SEPARATOR.join(line_parts).rstrip())
    lines.append("")
    lines.append("88 → Auto Mode (detect obf + deobfuscate)")
    lines.append("99 → EXIT")
    return "\n".join(lines)


def get_info_by_choice(choice: str) -> ObfuscationInfo | None:
    return MENU_CHOICES.get(choice)
