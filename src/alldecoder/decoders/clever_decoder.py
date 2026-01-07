import re
from ui.output import CliOutput 
from decoders.abstract_decoder import BaseDecodersClass

class CleverObfDeobfuscator(BaseDecodersClass):
    def decode(self) -> bool | None:
        try:
            source_pattern = re.compile(
                r"\(\s*lambda\s+__h\s*:\s*\(\s*__h\s*\(\s*\)\s*\)\s*\)\s*"
                r"\(\s*lambda\s*:\s*\(\s*\(\s*_lIlllIllII\s*\[\s*0\s*\]\s*==\s*0\s*\)\s*"
                r"and\s*\(\s*_lIlIlIllII\s*\(\s*0\s*,\s*1\s*\)\s*or\s*_lIllllII\s*"
                r"\(\s*_lIlIIIllII\s*\)\s*\)\s*\)\s*\)",
                re.DOTALL
            )

            if not self._match_obfuscation(source_pattern):
                return False

            crack_code = "print(_lIllIlIII)"
          
            self.content = source_pattern.sub(crack_code, self.content)
            self.content = self._capture_exec_output(self.content)

            self._write_result()            
            return True
            
        except Exception as e:
            self.output.print_error(e)
            return None
