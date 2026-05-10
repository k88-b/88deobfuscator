# -*- coding: utf-8 -*-

import zipfile
import subprocess
from ctypes import pythonapi
from core.abstract_decoder import BaseDecoder
from core.exceptions import DeobfuscationError


class ChristianObfDeobfuscator(BaseDecoder):
    def _load_content(self) -> str:
        return ""

    def _check_input_file(self) -> None:
        if not zipfile.is_zipfile(self.file_name):
            raise DeobfuscationError(
                f"The source file ({self.file_name}) is not obfuscated."
            )

        return

    def _check_obf(self, content: str) -> bool:
        try:
            if content:
                return bool(self.patterns.CHRISTIAN_OBF_LAYER_PATTERN.search(content))
            else:
                raise DeobfuscationError(
                    f"The source file ({self.file_name}) is not obfuscated."
                )

        except Exception as e:
            raise DeobfuscationError(f"Failed to check the obfuscated file: {e}")

    def _extract_and_decompile(self) -> None:
        try:
            with zipfile.ZipFile(self.file_name, "r") as zip_ref:
                file_list = zip_ref.namelist()
                if len(file_list) != 1:
                    raise ValueError(
                        f"The archive must contain exactly 1 file. Found: {len(file_list)}"
                    )
                zip_ref.extract(self.config.COMPILED_FILE, self.config.TEMP_DIR)
                compiled_file_path = self.file_manager.get_temp_path(
                    self.config.COMPILED_FILE
                )
                with open(self.temp_file_path, "w") as f:
                    subprocess.run(["pycdc", compiled_file_path], text=True, stdout=f)
        except Exception as e:
            raise DeobfuscationError(f"Failed to deobfuscate first layer: {e}")

    def _deobfuscate_layer(self) -> None:
        try:

            def hooked_exec(code, globals=None, locals=None) -> None:
                code = code.decode()
                if self.patterns.CHRISTIAN_OBF_TEMPLATE_PREFIX in code:
                    print(code.replace(self.patterns.CHRISTIAN_OBF_TEMPLATE_PREFIX, ""))
                else:
                    print(code)

            pythonapi.PyRun_SimpleString = hooked_exec

            self.content = self.code_executor.capture_exec_output(self.content)

        except Exception as e:
            raise DeobfuscationError(f"Failed to deobfuscate one of the layers: {e}")

    def decode(self) -> None:
        try:
            self._check_input_file()

            self.file_manager.create_temp_dir()

            self._extract_and_decompile()
            self.content = self.file_manager.read(self.temp_file_path)
            while self._check_obf(self.content):
                self._deobfuscate_layer()

            self._write_result()
            return

        except Exception as e:
            raise DeobfuscationError(f"Failed to deobfuscate the file: {e}")

        finally:
            self.file_manager.cleanup()
