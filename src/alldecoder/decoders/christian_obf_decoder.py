import re
import zipfile
import subprocess
import shutil
from ctypes import pythonapi
from typing import Optional
from decoders.abstract_decoder import BaseDecodersClass


class ChristianObfDeobfuscator(BaseDecodersClass):
    def _check_input_file(self) -> bool:
        return zipfile.is_zipfile(self.file_name)

    def _check_obf_file(self, file_name: str) -> bool:
        try:
            self.content = self._read_file(file_name)
            pattern = r"__import__\('ctypes'\)\.pythonapi\.PyRun_SimpleString"
            if self.content:
                match = re.search(pattern, self.content)
            return match is not None
        except Exception as e:
            self.output.print_error(f"Не удалось проверить обфусцированный файл: {e}")
            raise

    def _extract_and_decompile(self) -> None:
        try:
            with zipfile.ZipFile(self.file_name, "r") as zip_ref:
                file_list = zip_ref.namelist()
                if len(file_list) != 1:
                    raise ValueError(
                        f"В архиве должен быть ровно 1 файл. Найдено: {len(file_list)}"
                    )
                zip_ref.extract(self.COMPILED_FILE, self.TEMP_DIR)
                compiled_file_path = self._get_temp_path(self.COMPILED_FILE)
                with open(self.temp_file_path, "w") as f:
                    subprocess.run(["pycdc", compiled_file_path], text=True, stdout=f)
        except Exception as e:
            self.output.print_error(f"Не удалось деобфусцировать 1 слой: {e}")

    def _deobfuscate_layer(self) -> None:
        try:
            template_prefix = """
def globals():\n    return {'Easy protect by Christian F.': "easy protect by Christian F."}\n__import__('ctypes').pythonapi.PyRun_SimpleString(b'print("Easy protect by Christian F.")')"""

            def hooked_exec(code, globals=None, locals=None) -> None:
                self.content = code.decode()

            pythonapi.PyRun_SimpleString = hooked_exec
            with open(self.temp_file_path, "r") as f:
                script = f.read()
                if template_prefix in script:
                    self.content = script.replace(template_prefix, "")
                else:
                    exec(script)
                
            if self.content:
                self._write_file(self.temp_file_path, self.content)

        except Exception as e:
            self.output.print_error(f"Не удалось деобфусцировать один из слоев: {e}")

    def decode(self) -> Optional[bool]:
        try:
            if not self._check_input_file():
                self.output.print_error(f"Исходный файл ({self.file_name}) не обфусцирован.")
                raise SystemExit()

            self._extract_and_decompile()
            
            while self._check_obf_file(self.temp_file_path):
                self._deobfuscate_layer()

            shutil.copy(self.temp_file_path, self.new_file_name)
            return True

        except Exception as e:
            self.output.print_error(f"Не удалось деофбусцировать файл: {e}")
            return None

        finally:
            self._cleanup()
