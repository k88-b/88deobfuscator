# -*- coding: utf-8 -*-

import ast
import base64
import dis
import marshal
from types import CodeType
from core.abstract_decoder import BaseDecoder
from core.exceptions import DeobfuscationError


class ImpostorObfDeobfuscator(BaseDecoder):
    def _find_exec_string(self, code_obj: CodeType) -> str:
        instructions = list(dis.get_instructions(code_obj))

        for i, instr in enumerate(instructions):
            # Look for CALL or CALL_FUNCTION instructions
            if instr.opname not in ("CALL", "CALL_FUNCTION"):
                continue

            # Check if this is an exec() call
            exec_found = False
            for j in range(max(0, i - 10), i):
                prev_instr = instructions[j]
                if (
                    prev_instr.opname in ("LOAD_NAME", "LOAD_GLOBAL")
                    and prev_instr.argval == "exec"
                ):
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

        raise DeobfuscationError("Could not find exec string in bytecode")

    def _extract_encoded_data(self) -> bytes:
        match = self.patterns.IMPOSTOR_OBF_ENCODED_DATA_PATTERN.search(self.content)

        if not match:
            raise DeobfuscationError("Could not find Impostor encoded data in content")

        try:
            encoded_data = ast.literal_eval(match.group(1))

            decoded = base64.b85decode(encoded_data)
            decoded = base64.b64decode(decoded)
            decoded = base64.b32decode(decoded)
            decoded = base64.b16decode(decoded)

            if decoded is None:
                raise DeobfuscationError("Decoded data is empty")

            return decoded

        except Exception as e:
            raise DeobfuscationError(f"Failed to decode baseX chain: {e}")

    def _load_marshaled_data(self, data: bytes) -> CodeType:
        try:
            unmarshaled_data = marshal.loads(data)
            if unmarshaled_data is None:
                raise DeobfuscationError("Unmarshaled data is empty.")

            return unmarshaled_data

        except Exception as e:
            raise DeobfuscationError(f"Failed to unmarshal code object: {e}")

    def decode(self) -> None:
        try:
            self.match = self.pattern_matcher.match_obfuscation(
                self.patterns.IMPOSTOR_OBF_PATTERN, content=self.content
            )

            print(
                "\nWARNING: Deobfuscator should be run using the same Python version that was used for obfuscation"
            )
            print(
                "Using mismatched Python versions may cause decoding errors or unexpected behavior\n"
            )

            decoded_data = self._extract_encoded_data()
            code_obj = self._load_marshaled_data(decoded_data)
            exec_string = self._find_exec_string(code_obj)
            self.content = exec_string

            self._write_result()
            return

        except Exception as e:
            raise DeobfuscationError(e)
