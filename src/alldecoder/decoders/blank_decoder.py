# -*- coding: utf-8 -*-

import re
from abc import ABC, abstractmethod
from typing import Type
from ui.output import CliOutput
from core.abstract_decoder import BaseDecodersClass
from core.code_executor import CodeExecutor


class Decoder(ABC):
    def __init__(
        self, cli_output: CliOutput, code_executor: CodeExecutor, content: str = ""
    ) -> None:
        self.content = content
        self.output = cli_output
        self.code_executor = code_executor

    def _replace_bytes(self) -> None:
        self.content = self.content.replace(
            "99, 101, 120, 101", "116, 110, 105, 114, 112"
        )

    @abstractmethod
    def deobfuscate(self):
        pass


class FirstLayer(Decoder):
    def deobfuscate(self) -> str:
        self._replace_bytes()
        self.content = self.content.replace(")))", ")).decode())")

        return self.code_executor.capture_exec_output(self.content)


class SecondLayer(Decoder):
    def deobfuscate(self):
        self._replace_bytes()
        self.content = self.content.replace("]))))", "]))).decode())")

        return self.code_executor.capture_exec_output(self.content)


class ThirdLayer(Decoder):
    def deobfuscate(self):
        pattern = r"(.*?)\s*=\s*\[.*?\]"
        match = re.search(pattern, self.content)
        if match:
            ip_table_name = match.group(1)
        else:
            raise ValueError("Failed to find ip_table.")

        self.content = self.content.strip().split("\n")
        self.content[-1] = (
            f'\ndata = list([int(x) for item in [value.split(".") for value in {ip_table_name}] for x in item])\nprint(__import__("zlib").decompress(__import__("base64").b64decode(bytes(data))).decode())'
        )
        self.content = "\n".join(self.content)

        return self.code_executor.capture_exec_output(self.content)


class BlankObfDeobfuscator(BaseDecodersClass):
    SOURCE_PATTERN = re.compile(
        r"bytes\(\[108,\s?97,\s?118,\s?101\]\[::-1\]\).decode\(\)\)\(bytes\(\[99,\s?101,\s?120,\s?101\]\[::-1\]\)\)"
    )

    def _define_layer(self) -> str | None:
        layer = self.content
        if (
            "in getattr(__import__(bytes([115, 110, 105, 116, 108, 105, 117, 98][::-1]).decode()), bytes([108, 97, 118, 101][::-1]).decode())(bytes([101, 103, 110, 97, 114][::-1]))"
            in layer
        ):
            return "2"
        elif re.search(r"\[\s*('(?:\d{1,3}\.){3}\d{1,3}'\s*,\s*)+", layer):
            return "3"
        elif "[99, 101, 120, 101]" in layer:
            return "1"
        else:
            return None

    def decode(self) -> bool | None:
        try:
            if not self.pattern_matcher.match_obfuscation(
                self.SOURCE_PATTERN, content=self.content
            ):
                return False

            layer_classes_dict: dict[str, Type[Decoder]] = {
                "1": FirstLayer,
                "2": SecondLayer,
                "3": ThirdLayer,
            }

            layer_decoder = None

            try:
                while (layer := self._define_layer()) is not None:
                    layer_decoder = layer_classes_dict[layer](
                        content=self.content,
                        cli_output=self.output,
                        code_executor=self.code_executor,
                    )
                    self.content = layer_decoder.deobfuscate()

            except Exception as e:
                self.output.print_error(
                    f"Deobfuscation of layer {layer_decoder.__class__.__name__} failed: {e}"
                )
                return None

            self._write_result()
            return True

        except Exception as e:
            self.output.print_error(e)
            return None
