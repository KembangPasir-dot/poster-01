"""Copy the bundled entry.png to the grader's output directory.

The poster itself (VISIT KRZVANIA) is rendered during the build from
poster.html and committed as entry.png. This program only copies that
file, using the standard library alone, so it runs in the grader's
stock python:3.13 sandbox with no network and no third-party packages.

The copy is verified, not trusted: the destination must exist, match
the source byte-for-byte in size, and match its SHA-256 digest.
"""

import hashlib
import os
import shutil
from pathlib import Path

IMAGE_NAME = "entry.png"

# The competition caps the entry image at 1 MiB; refuse anything larger
# rather than copying a wrong file out as the entry.
MAX_BYTES = 1_048_576

# Paths are resolved from this file, never from the working directory:
# the grader may run the entry from anywhere.
BASE_DIR = Path(__file__).resolve().parent
SOURCE = BASE_DIR / IMAGE_NAME

# MAKEFUN_OUTPUT_DIR is honoured when set; the grader default is /output.
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def sha256_of(path):
    """Return the hex SHA-256 digest of the file at *path*."""
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def copy_and_verify(source, output_dir):
    """Copy *source* into *output_dir* and verify the copy.

    Returns (destination, size, sha256). Raises ValueError on any
    mismatch between the source and the copy.
    """
    if not source.exists():
        raise ValueError(f"Source image missing: {source}")
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / source.name
    shutil.copyfile(source, destination)
    if not destination.exists():
        raise ValueError("Destination does not exist after copy")
    size = destination.stat().st_size
    if size > MAX_BYTES:
        raise ValueError(
            f"Destination size {size} exceeds the {MAX_BYTES} byte cap"
        )
    if size != source.stat().st_size:
        raise ValueError(
            f"Destination size {size} differs from source "
            f"{source.stat().st_size}"
        )
    source_sha256 = sha256_of(source)
    copied_sha256 = sha256_of(destination)
    if copied_sha256 != source_sha256:
        raise ValueError("Destination SHA-256 differs from source")
    return destination, size, copied_sha256


def main():
    destination, size, sha256 = copy_and_verify(SOURCE, OUTPUT_DIR)
    return destination, size, sha256


if __name__ == "__main__":
    destination, size, sha256 = main()
    print(f"{destination.name}: {size} bytes, SHA-256 {sha256}")
