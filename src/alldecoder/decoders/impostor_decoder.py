# -*- coding: utf-8 -*-

import ast
import base64
import dis
import marshal
import re
from types import CodeType
from typing import Optional

from decoders.abstract_decoder import BaseDecodersClass


class ImpostorObfDeobfuscator(BaseDecodersClass):
    SOURCE_PATTERN = re.compile(
        r"(\.b(?:16|64)decode\([^)]+\))"
        r"|(eval\s*\([^)]*chr\([^)]+\))"
        r"|(exec\s*\([^)]*__globals[^)]*\))"
        r"|(Gateway\([^)]*\))"
        r"|(__tunnel\s*\([^)]*->\s*Gateway)"
        r"|(__module_?_?[^=]*=)"
    )
    
    def _find_exec_string(self, code_obj: CodeType) -> Optional[str]:
        instructions = list(dis.get_instructions(code_obj))
        
        for i, instr in enumerate(instructions):
            # Look for CALL or CALL_FUNCTION instructions
            if instr.opname not in ("CALL", "CALL_FUNCTION"):
                continue
                
            # Check if this is an exec() call
            exec_found = False
            for j in range(max(0, i-10), i):
                prev_instr = instructions[j]
                if (prev_instr.opname in ("LOAD_NAME", "LOAD_GLOBAL") and 
                    prev_instr.argval == "exec"):
                    exec_found = True
                    break
            
            if not exec_found:
                continue
            
            # Collect constants loaded before the exec call
            constants = []
            for k in range(j + 1, i):
                if instructions[k].opname == "LOAD_CONST":
                    const_val = instructions[k].argval
                    constants.append(const_val)
            
            # Return the first string constant
            for const in constants:
                if isinstance(const, str):
                    return const
        
        return None

    def _extract_encoded_data(self) -> Optional[bytes]:
        pattern = r"Interpreter\((b[\"'][^']*[\"'])"
        match = re.search(pattern, self.content)

        if not match:
            self.output.print_error("Could not find Impostor encoded data in content")
            return None

        try:        
            encoded_data = ast.literal_eval(match.group(1))

            decoded = base64.b85decode(encoded_data)
            decoded = base64.b64decode(decoded)
            decoded = base64.b32decode(decoded)
            decoded = base64.b16decode(decoded)
            return decoded

        except Exception as e:
            self.output.print_error(f"Failed to decode baseX chain: {e}")
            return None

    def _load_marshaled_data(self, data: bytes) -> Optional[CodeType]:
        try:
            return marshal.loads(data)
        except Exception as e:
            self.output.print_error(f"Failed to unmarshal code object: {e}")
            return None

    def decode(self) -> Optional[bool]:
        try:
            if not self._match_obfuscation(self.SOURCE_PATTERN):
                return False

            print("\nWARNING: Deobfuscator should be run using the same Python version that was used for obfuscation")
            print("Using mismatched Python versions may cause decoding errors or unexpected behavior\n")

            decoded_data = self._extract_encoded_data()
            if decoded_data is None:
                return False

            code_obj = self._load_marshaled_data(decoded_data)
            if code_obj is None:
                return False

            exec_string = self._find_exec_string(code_obj)
            if exec_string is None:
                self.output.print_error("Could not find exec string in bytecode")
                return False

            self.content = exec_string
            
            self._write_result()            
            return True
            
        except Exception as e:
            self.output.print_error(e)
            return None
