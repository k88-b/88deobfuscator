# -*- coding: utf-8 -*-

import ast
import re
import os
import lzma
import zlib
from typing import Optional, Tuple, List
from decoders.abstract_decoder import BaseDecodersClass


class Ne4toObfDeobfuscator(BaseDecodersClass):        
    def _check_input_file(self) -> bool:
        try:
            self.content = self._read_file(self.file_name)
            pattern = r"encrypted_bytes\s=\s\["
            match = re.search(pattern, self.content)
            if match:
                return True
            else:
                return False
        except Exception as e:
            self.output.print_error(f"Не удалось проверить исходный файл: {e}")
            raise

    def _check_obf_file(self, fname: str) -> bool:
        try:
            self.content = self._read_file(fname)
            pattern = r"exec\(loads\(b"
            match = re.search(pattern, self.content)
            if match:
                return True
            else:
                return False
        except Exception as e:
            self.output.print_error(f"Не удалось проверить обфусцированный файл: {e}")
            raise

    def _replace_marshal(self) -> None:
        self.content = self.content.replace(
            "exec(loads", 
            "x = (__import__('marshal').loads"
        )
        self.content += r"""
import dis, marshal
magic = b'\xa7\r\r\n\x00\x00\x00\x00\x04\x94\x90d\xd4`\x00\x00'
        
with open('.temp_decode.pyc', 'wb') as pyc:
    pyc.write(magic)
    marshal.dump(dis.Bytecode(x).codeobj,pyc)"""

    def _extract_pattern(self, pattern: str, description: str) -> Optional[str]:
        match = re.search(pattern, self.content)
        if not match:
            self.output.print_error(f"Не найдено {description} в байткоде.")
            return None
        return match.group(1)

    def _extract_content_from_bytes(self) -> Tuple[str, List[int]]:
        masks = self._extract_pattern(
            r"\s*24\s*LOAD\_CONST\s*4\:\s\((.*?)\)", 
            "masks"
        )
        bytes_str = self._extract_pattern(
            r"\s*36\s*LOAD_CONST\s*5\:\s\((.*?)\)", 
            "bytes"
        )
        if masks is None or bytes_str is None:
            raise ValueError("Incorrect bytecode format.")

        bytes_ = [int(i.strip()) for i in bytes_str.split(",")]
        return masks, bytes_

    def decode(self) -> bool | None:
        try:
            if not self._check_input_file():
                self.output.print_error(f"Исходный файл ({self.file_name}) не обфусцирован.")
                raise SystemExit()
                return None

            match = re.search(
                r"getattr\(\_\_builtins\_\_\,\s.*\)\(.*\)",
                self.content
            )
            if not match:
                raise ValueError("Incorrect input code.")
            self.content = self.content.replace(
                match.group(0),
                "byte_array = [eval(expr) for expr in encrypted_bytes]\nprint(bytes(byte_array).decode('utf-8'))"
            )
            self._write_file(file_name=".temp_decode.py", content=self.content)
            os.system("python3 .temp_decode.py > .tempp_decode.py")
            try:
                while True:
                    if not self._check_obf_file(".tempp_decode.py"):
                        self.output.print_error("Не удалось найти паттерн в обфусцированном файле.")
                        return None

                    self._replace_marshal()
                    self._write_file(file_name=".temp_decode.py", content=self.content)
                    os.system("python3 .temp_decode.py")
                    os.system("pycdas .temp_decode.pyc > .tempp_decode.py")
                    self.content = self._read_file(".tempp_decode.py")
                    bytes_str = re.search(
                        r"""
\s*70\s*LOAD_CONST\s*2\:\s(.*)""",
                        self.content,
                    )
                    if bytes_str:
                        bytes_ = ast.literal_eval(bytes_str.group(1))
                    else:
                        self.output.print_error("Не удалось извлечь байты из байткода.")
                    self.content = zlib.decompress(lzma.decompress(bytes_)).decode()
                    self._write_file(file_name=".tempp_decode.py", content=self.content)
            except AttributeError:
                print("Все слои с маршалом были успешно деобфусцированы.")
            self.content = self._read_file(".tempp_decode.py")
            self.masks, self.bytes_ = self._extract_content_from_bytes()
            self.content = f"""
masks = [{self.masks}]
bts = {self.bytes_}
def xorb(content, mask):
    b = []
    for x in content:
        b.append(x ^ mask)
    return bytes(b)
def decode(encoded, masks):
    data = encoded
    for mask in masks[::-1]:
        data = xorb(data, mask)
    return data
try:
    print(decode(bts, masks).decode())
except Exception as e:
    print(f"Error! {{e}}")
    """
            self._write_file(file_name=".temp_decode.py", content=self.content)
            os.system(f"python3 .temp_decode.py > '{self.new_file_name}'")

            return True

        except Exception as e:
            self.output.print_error(f"Не удалось деобфусцировать файл: {e}")
            return None
        finally:
            for file in [".temp_decode.py", ".temp_decode.pyc", ".tempp_decode.py"]:
                if os.path.exists(file):
                    os.remove(file)
