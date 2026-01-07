**88 Deobfuscator**

**Supported Obfuscations:**
- **Base:** base64, base32, base16
- **Compressions:** zlib, gzip, lzma
- **Combinations:** base + compression
- **Specific:** RendyObf, BlankObfv2, ChristianObf
- **Auto-detection:** automatic recognition of the obfuscation type


**Installation & Run::**

    git clone https://github.com/k88-b/88deobfuscator.git
    cd 88deobfuscator
    uv sync
    uv run src/alldecoder/main.py

Deobfuscating ChristianObf requires [pycdc](https://github.com/zrax/pycdc).

**Before/After Example::**

<div align="left">
  <img src="https://github.com/user-attachments/assets/b29407e1-0928-4725-9d78-48fb79c4c6c8" width="45%" />
  <img src="https://github.com/user-attachments/assets/8c666492-0156-4e22-b1e4-b38a30e787c7" width="45%" />
</div>


