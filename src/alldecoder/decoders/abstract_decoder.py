# -*- coding: utf-8 -*-

import re
import os
import shutil
import subprocess
from abc import ABC, abstractmethod
from typing import Optional
from ui import CliOutput
from core.config import EXEC_PATTERN, COMMENTS_PATTERN, NOTE, TEMP_DIR, TEMP_FILE, COMPILED_FILE


class BaseDecodersClass(ABC):    
    def __init__(
        self,
        file_name: str,
        new_file_name: str,
        cli_output: CliOutput,
        user_choice: str=""
    ):
        self.EXEC_PATTERN = EXEC_PATTERN
        self.COMMENTS_PATTERN = COMMENTS_PATTERN
        self.NOTE = NOTE
        self.TEMP_DIR = TEMP_DIR
        self.TEMP_FILE = TEMP_FILE
        self.COMPILED_FILE = COMPILED_FILE
        self.file_name = file_name
        self.new_file_name = new_file_name
        self.user_choice = user_choice
        self.content = ""
        self.output = cli_output
        self.temp_file_path = self._get_temp_path(self.TEMP_FILE)

    def _get_temp_path(self, filename: str) -> str:
        return os.path.join(self.TEMP_DIR, filename)

    def _write_file(self, file_name: str, content: str) -> bool:
        try:
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(content)
                return True
        except Exception as e:
            self.output.print_error(f"Не удалось записать контент в файл {file_name}: {e}")
            return False
    
    def _read_file(self, file_name: str) -> str:
        try:
            with open(file_name, "r", encoding="utf-8") as f:
                    return f.read()
        except Exception as e:
            self.output.print_error(f"Не удалось прочитать содержимое файла {file_name}: {e}")
            raise SystemExit()

    def _cleanup(self) -> None:
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)
        else:
            self.output.print_error("Директория .tempdir не удалена.")

    def _redirect_python_output(self, source_file: str, output_file: str) -> bool:
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                subprocess.run(
                    ["python3", source_file],
                    stdout=f,
                    text=True
                )
                return True
        except Exception as e:
            self.output.print_error(f"Не удалось перенаправить вывод из временного файла: {e}")
            return False
        
    def _match_obfuscation(self, pattern: str) -> bool:
        with open(self.file_name, "r", encoding="utf-8") as f:
            self.content = f.read()
            
        self.match = re.search(pattern, self.content)
        if not self.match:
            self.output.print_error("Обфускация не обнаружена.")
            return False
        return True

    def _remove_comments(self) -> None:
        try:
            while re.search(
                self.COMMENTS_PATTERN, self.content
            ):
                 self.content = re.sub(
                    self.COMMENTS_PATTERN, "", self.content
                )
        except Exception as e:
            self.output.print_error(f"Не удалось удалить комментарии: {e}")

    def _process_content(self) -> None:
        try: 
            while re.search(
                self.EXEC_PATTERN, self.content
            ):
                self.content = re.sub(
                    self.EXEC_PATTERN, lambda m: self.decode_layer(m.group(1)), self.content
                )
        except Exception as e:
            self.output.print_error(f"Не удалось обработать код на одном из слоев: {e}")

    def _write_result(self) -> None:
        try:
            self._write_file(
                file_name=self.new_file_name,
                content=self.NOTE + self.content.strip()
            )            
        except Exception as e:
            self.output.print_error(f"Не удалось записать финальный результат в файл: {e}")
    
    def common_decode_logic(self, pattern: str, clean_pattern: str) -> bool:
        if not self._match_obfuscation(pattern):
            return False
        self._process_content()
        self.content = self.content.replace(
            clean_pattern, ""
        )
        self._remove_comments()
        self._write_result()    
        return True
    
    def decode_layer(self, encoded_str: str) -> Optional[str]:
        pass
        
    @abstractmethod
    def decode(self):
        pass
