# -*- coding: utf-8 -*-

import ast
import marshal
import gzip
import lzma
import zlib
import base64
import re
from decoders.abstract_decoder import BaseDecodersClass


class RendyDecoder(BaseDecodersClass):
    SOURCE_PATTERN = re.compile(
        r"_=lambda __:__import__\('marshal'\)\.loads\("
        r"__import__\('gzip'\)\.decompress\("
        r"__import__\('lzma'\)\.decompress\("
        r"__import__\('zlib'\)\.decompress\("
        r"__import__\('base64'\)\.b64decode\("
        r"__\[::-1\]\)\)\)\)\);exec\(_\('(.*?)'\)\)"
    )

    def decode(self):
        try:
            if not self._match_obfuscation(self.SOURCE_PATTERN):
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
                self.output.print_error("Failed to get the result from the temporary file.")
                return False

        except Exception as e:
            self.output.print_error(f"Failed to deobfuscate the file: {e}")
            return False

    
