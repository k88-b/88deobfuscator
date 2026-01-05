**88 Deobfuscator**
Python-инструмент для деобфускации файлов, защищенных популярными видами обфускаций.

**Поддерживаемые обфускации:**
- **Base:** base64, base32, base16
- **Компрессии:** zlib, gzip, lzma
- **Комбинации:** base + compression
- **Специфичные:** RendyObf, Ne4toObf, BlankObfv2, ChristianObf
- **Автоопределение:** автоматическое распознавание типа обфускации


**Установка и запуск:**

    git clone https://github.com/k88-b/88deobfuscator.git
    cd 88deobfuscator
    uv sync
    uv run src/alldecoder/main.py

Для деобфускации Ne4toObf и ChristianObf требуется [pycdc](https://github.com/zrax/pycdc).

**Пример до/после:**

<div align="left">
  <img src="https://github.com/user-attachments/assets/b29407e1-0928-4725-9d78-48fb79c4c6c8" width="45%" />
  <img src="https://github.com/user-attachments/assets/8c666492-0156-4e22-b1e4-b38a30e787c7" width="45%" />
</div>
