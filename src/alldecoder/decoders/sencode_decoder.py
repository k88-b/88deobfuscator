# -*- coding: utf-8 -*-

# !! NOT USING !!

import subprocess
from decoders.abstract_decoder import BaseDecodersClass

class SEncodeDecoder(BaseDecodersClass):
    def decode(self):
        command = ["pycdc", self.file_name]
        try:
            result = subprocess.run(command, capture_output=True, text=True)        
            
            if result.returncode != 0:
                self.output.print_error("Декомпиляция не удалась:")
                print(result.stderr)

            else:
                temp_file = ".temp_decode.py"
                self._write_file(file_name=temp_file, content=result.stdout)
    
                print(f"Декомпилированный код сохранен в {temp_file}")
                self.content = self._read_file(temp_file)
                self.content = self.content.replace("exec(str(chr(35) + chr(1)))", "")
                self.content = self.content.replace("chr(None(35)(chr + None(1)))", "")
                self.content = self.content.replace("# WARNING: Decompyle incomplete", "result = ''.join(chr(i) for i in _)")
                self.content = self.content.replace(")(_()))", "print(result)")

                self._write_file(file_name=temp_file, content=self.content)
                    
                print(f"Замены выполнены в файле {temp_file}")

                with open(self.new_file_name, "w", encoding="utf-8") as f:
                    subprocess.run(["python", temp_file], stdout=f, stderr=subprocess.STDOUT)

        except Exception as e:
            self.output.print_error(e)
