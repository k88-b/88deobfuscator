# -*- coding: utf-8 -*-

import ast
import marshal
import gzip
import lzma
import zlib
import base64
from decoders.abstract_decoder import BaseDecodersClass


class RendyDecoder(BaseDecodersClass):
    def decode(self):
        try:
            pattern = r"_=lambda __:__import__\('marshal'\)\.loads\(__import__\('gzip'\)\.decompress\(__import__\('lzma'\)\.decompress\(__import__\('zlib'\)\.decompress\(__import__\('base64'\)\.b64decode\(__\[::-1\]\)\)\)\)\);exec\(_\('(.*?)'\)\)"
            if not self._match_obfuscation(pattern):
                return False
                
            encoded = self.match.group(1)
            encoded = ast.literal_eval(f"b'{encoded}'")
            self.content = base64.b64decode(encoded[::-1])                  
            self.content = zlib.decompress(self.content)                   
            self.content = lzma.decompress(self.content)                   
            self.content = gzip.decompress(self.content)                   
            self.content = marshal.loads(self.content).decode()              
            self._remove_comments()
            if self.content:
                self._write_result()
                return True

            else:
                self.output.print_error("Не удалось получить результат из времменного файла.")
                return False

        except Exception as e:
            self.output.print_error(f"Не удалось деобфусцировать файл: {e}")
            return False

    
