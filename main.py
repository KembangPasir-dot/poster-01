"""Copy the bundled entry.png to /output/entry.png.

The poster itself (VISIT KRZVANIA) is rendered during the build from
poster.html and committed as entry.png; this program only copies it,
using the standard library, so it runs in the grader's stock sandbox.
"""

import hashlib
import os
import shutil
from pathlib import Path

IMAGE_NAME = "entry.png"
BASE_DIR = Path(__file__).resolve().parent
SRC = BASE_DIR / IMAGE_NAME
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    destination = OUT_DIR / IMAGE_NAME
    shutil.copyfile(SRC, destination)
    if not destination.exists():
        raise ValueError("Destination does not exist")
    size = destination.stat().st_size
    if size != SRC.stat().st_size:
        raise ValueError("Destination size differs from source")
    with SRC.open("rb") as source_file:
        source_sha256 = hashlib.file_digest(source_file, "sha256").hexdigest()
    with destination.open("rb") as destination_file:
        sha256 = hashlib.file_digest(destination_file, "sha256").hexdigest()
    if sha256 != source_sha256:
        raise ValueError("Destination SHA-256 differs from source")
    return destination, size, sha256


if __name__ == "__main__":
    destination, size, sha256 = main()
    print(f"{destination.name}: {size} bytes, SHA-256 {sha256}")
