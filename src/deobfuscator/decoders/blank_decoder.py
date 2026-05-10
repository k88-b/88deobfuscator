# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Type
from ui.output import CliOutput
from core.abstract_decoder import BaseDecoder
from core.code_executor import CodeExecutor
from core.patterns import Patterns
from core.exceptions import DeobfuscationError


class Decoder(ABC):
    def __init__(
        self,
        cli_output: CliOutput,
        code_executor: CodeExecutor,
        patterns: Patterns,
        content: str = "",
    ) -> None:
        self.content = content
        self.output = cli_output
        self.code_executor = code_executor
        self.patterns = patterns

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
        match = self.patterns.BLANK_OBF_THIRD_LAYER_DEOBFUSCATION_PATTERN.search(
            self.content
        )
        if match:
            ip_table_name = match.group(1)
        else:
            raise DeobfuscationError("Failed to find ip_table.")

        self.content = self.content.strip().split("\n")
        self.content[-1] = (
            f'\ndata = list([int(x) for item in [value.split(".") for value in {ip_table_name}] for x in item])\nprint(__import__("zlib").decompress(__import__("base64").b64decode(bytes(data))).decode())'
        )
        self.content = "\n".join(self.content)

        return self.code_executor.capture_exec_output(self.content)


class BlankObfDeobfuscator(BaseDecoder):
    def _define_layer(self) -> str | None:
        layer = self.content
        if self.patterns.BLANK_OBF_SECOND_LAYER_PATTERN in layer:
            return "2"
        elif self.patterns.BLANK_OBF_THIRD_LAYER_PATTERN.search(layer):
            return "3"
        elif self.patterns.BLANK_OBF_FIRST_LAYER_PATTERN in layer:
            return "1"
        else:
            return None

    def decode(self) -> None:
        try:
            self.pattern_matcher.match_obfuscation(
                self.patterns.BLANK_OBF_PATTERN, content=self.content
            )

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
                        patterns=self.patterns,
                    )
                    self.content = layer_decoder.deobfuscate()

            except Exception as e:
                raise DeobfuscationError(
                    f"Deobfuscation of layer {layer_decoder.__class__.__name__} failed: {e}"
                )

            self._write_result()
            return

        except Exception as e:
            raise DeobfuscationError(e)
