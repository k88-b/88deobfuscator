# -*- coding: utf-8 -*-

import re
import zipfile
import subprocess
from ctypes import pythonapi
from typing import Optional
from decoders.abstract_decoder import BaseDecodersClass
from core.config import CHRISTIAN_OBF_TEMPLATE_PREFIX as TEMPLATE_PREFIX


class ChristianObfDeobfuscator(BaseDecodersClass):
    LAYER_PATTERN = re.compile(r"__import__\('ctypes'\)\.pythonapi\.PyRun_SimpleString")

    def _check_input_file(self) -> bool:
        return zipfile.is_zipfile(self.file_name)

    def _check_obf(self, content: str) -> bool:
        try:
            if content:
                return bool(self.LAYER_PATTERN.search(content))
            else:
                return False
        except Exception as e:
            self.output.print_error(f"Failed to check the obfuscated file: {e}")
            raise

    def _extract_and_decompile(self) -> None:
        try:
            with zipfile.ZipFile(self.file_name, "r") as zip_ref:
                file_list = zip_ref.namelist()
                if len(file_list) != 1:
                    raise ValueError(
                        f"The archive must contain exactly 1 file. Found: {len(file_list)}"
                    )
                zip_ref.extract(self.COMPILED_FILE, self.TEMP_DIR)
                compiled_file_path = self._get_temp_path(self.COMPILED_FILE)
                with open(self.temp_file_path, "w") as f:
                    subprocess.run(["pycdc", compiled_file_path], text=True, stdout=f)
        except Exception as e:
            self.output.print_error(f"Failed to deobfuscate first layer: {e}")

    def _deobfuscate_layer(self) -> None:
        try:
            def hooked_exec(code, globals=None, locals=None) -> None:
                code = code.decode()
                if TEMPLATE_PREFIX in code:
                    print(code.replace(TEMPLATE_PREFIX, ""))
                else:
                    print(code)
                
            pythonapi.PyRun_SimpleString = hooked_exec
      
            self.content = self._capture_exec_output(self.content)

        except Exception as e:
            self.output.print_error(f"Failed to deobfuscate one of the layers: {e}")

    def decode(self) -> Optional[bool]:
        try:
            if not self._check_input_file():
                self.output.print_error(f"The source file ({self.file_name}) is not obfuscated.")
                raise SystemExit()

            self._extract_and_decompile()
            self.content = self._read_file(self.temp_file_path)
            while self._check_obf(self.content):
                self._deobfuscate_layer()

            self._write_result()
            return True

        except Exception as e:
            self.output.print_error(f"Failed to deobfuscate the file: {e}")
            return None

        finally:
            self._cleanup()
