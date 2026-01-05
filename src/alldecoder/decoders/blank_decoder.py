# -*- coding: utf-8 -*-

import re
import os
import io
import subprocess
import sys
from abc import ABC, abstractmethod
from contextlib import redirect_stdout
from typing import List, Union, Type
from ui.output import CliOutput 
from decoders.abstract_decoder import BaseDecodersClass

class Decoder(ABC):
    def __init__(self, cli_output: CliOutput, content: str = "") -> None:
        self.content = content
        self.output = cli_output

    def _read_file(self, file_name: str, mode: str = "") -> Union[str, List[str]]:
        try:
            with open(file_name, "r", encoding="utf-8") as f:
                if mode == "lines":
                    return f.readlines()
                else:
                    return f.read()
        except Exception as e:
            self.output.print_error(f"Не удалось прочитать содержимое файла {file_name}: {e}")
            raise

    def _write_file(self, file_name: str, content: str, mode: str = "") -> bool:
        try:
            with open(file_name, "w", encoding="utf-8") as f:
                if mode == "lines":
                    f.writelines(content)
                else:
                    f.write(content)
                return True
        except Exception as e:
            self.output.print_error(f"Не удалось записать контент в файл {file_name}: {e}")
            return False

    def _capture_exec_output(self) -> str:
        namespace = {}
        f = io.StringIO()
        with redirect_stdout(f):
            exec(self.content, namespace, namespace)
        return f.getvalue().strip()

    def _replace_bytes(self) -> None:
        self.content = self.content.replace(
            "99, 101, 120, 101",
            "116, 110, 105, 114, 112"
        )

    @abstractmethod
    def deobfuscate(self):
        pass


class FirstLayer(Decoder):
    def deobfuscate(self) -> str:
        self._replace_bytes()
        self.content = self.content.replace(
            ")))", 
            ")).decode())"
        )
        
        return self._capture_exec_output()

class SecondLayer(Decoder):
    def deobfuscate(self):
        self._replace_bytes()
        self.content = self.content.replace(
            "]))))", 
            "]))).decode())"
        )

        return self._capture_exec_output()


class ThirdLayer(Decoder):
    def deobfuscate(self):
        pattern = r"(.*?)\s*=\s*\[.*?\]"
        match = re.search(pattern, self.content)
        if match:
            ip_table_name = match.group(1)
        else:
            raise ValueError("Не удалось найти ip_table.")

        self.content = self.content.strip().split('\n')
        self.content[-1] = f"\ndata = list([int(x) for item in [value.split(\".\") for value in {ip_table_name}] for x in item])\nprint(__import__(\"zlib\").decompress(__import__(\"base64\").b64decode(bytes(data))).decode())"
        self.content = '\n'.join(self.content)

        return self._capture_exec_output()

class BlankObfDeobfuscator(BaseDecodersClass):
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
            if not self._match_obfuscation(r"bytes\(\[108,\s?97,\s?118,\s?101\]\[::-1\]\).decode\(\)\)\(bytes\(\[99,\s?101,\s?120,\s?101\]\[::-1\]\)\)"):
                self.output.print_error(f"Исходный файл ({self.file_name}) не обфусцирован.")
                return None

            layer_classes_dict: dict[str, Type[Decoder]] = {
                "1": FirstLayer,
                "2": SecondLayer,
                "3": ThirdLayer,
            }
            try:
                while (layer := self._define_layer()) is not None:
                    print(f"Деобфускация слоя: {layer}")
                    layer_decoder = layer_classes_dict[layer](content=self.content, cli_output=self.output)
                    self.content = layer_decoder.deobfuscate()

            except Exception as e:
                self.output.print_error(
                    f"Дебфускация слоя {layer_decoder.__class__.__name__} не удалась: {e}"
                )
                return None

            self._write_result()
            return True

        except Exception as e:
            self.output.print_error(e)
            return None


                    
