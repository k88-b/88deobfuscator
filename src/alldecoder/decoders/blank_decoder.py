# -*- coding: utf-8 -*-

import re
import os
import subprocess
from abc import ABC, abstractmethod
from typing import List, Union, Type
from core.config import NOTE
from ui.output import CliOutput 


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

    def _redirect_python_output(self, source_file: str, output_file: str) -> bool:
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                subprocess.run(["python3", source_file], stdout=f, text=True)
                return True
        except Exception as e:
            self.output.print_error(f"Не удалось перенаправить вывод из временного файла: {e}")
            return False

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
        self._write_file(file_name=".temp_decode.py", content=self.content)
        self._redirect_python_output(".temp_decode.py", ".tempp_decode.py")
        return self._read_file(".tempp_decode.py")


class SecondLayer(Decoder):
    def deobfuscate(self):
        self._replace_bytes()
        self.content = self.content.replace(
            "]))))", 
            "]))).decode())"
        )
        self._write_file(file_name=".temp_decode.py", content=self.content)
        self._redirect_python_output(".temp_decode.py", ".tempp_decode.py")
        return self._read_file(".tempp_decode.py")


class ThirdLayer(Decoder):
    def deobfuscate(self):
        self.content = self._read_file(file_name=".tempp_decode.py", mode="lines")
        pattern = r"(.*?)\s*=\s*\[.*?\]"
        match = re.search(pattern, self.content[0])
        if match:
            ip_table_name = match.group(1)
        else:
            raise ValueError("Не удалось найти ip_table.")
        self.content[-1] = (
            f"data = list([int(x) for item in [value.split(\".\") for value in {ip_table_name}] for x in item])\nprint(__import__(\"zlib\").decompress(__import__(\"base64\").b64decode(bytes(data))).decode())"
        )
        self._write_file(file_name=".temp_decode.py", content=self.content, mode="lines")
        self._redirect_python_output(".temp_decode.py", ".tempp_decode.py")
        return self._read_file(".tempp_decode.py")


class BlankObfDeobfuscator:
    def __init__(self, file_name: str, new_file_name: str, user_choice: str, cli_output: CliOutput) -> None:
        self.file_name = file_name
        self.new_file_name = new_file_name
        self.content = ""
        self.output = cli_output
        self.NOTE = NOTE

    def _check_input_file(self) -> bool:
        try:
            with open(self.file_name, "r", encoding="utf-8") as f:
                self.content = f.read()

            pattern = r"bytes\(\[108,\s?97,\s?118,\s?101\]\[::-1\]\).decode\(\)\)\(bytes\(\[99,\s?101,\s?120,\s?101\]\[::-1\]\)\)"
            match = re.search(pattern, self.content)
            if match:
                return True
            else:
                return False

        except Exception as e:
            self.output.print_error(f"Ошибка с проверкой исходного файла: {e}")
            return False

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
            if not self._check_input_file():
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

            with open(self.new_file_name, "w", encoding="utf-8") as f:
                f.write(self.NOTE + self.content)
            return True

        except Exception as e:
            self.output.print_error(e)
            return None

        finally:
            for file in [".temp_decode.py", ".tempp_decode.py", ".temp_decode.pyc"]:
                if os.path.exists(file):
                    os.remove(file)

                    
