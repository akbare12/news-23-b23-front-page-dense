#!/usr/bin/env python3
"""Copy entry.png to MAKEFUN_OUTPUT_DIR/entry.png.

The grader runs this program with a read-only repository and a writable
output directory, so the program must never write next to itself:
the only output is os.environ["MAKEFUN_OUTPUT_DIR"]/entry.png
"""
import hashlib
import os
import shutil
import struct
import sys


def main():
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as fh:
        data = fh.read()
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        print(f"entry.png is {width}x{height}, expected 1024x1024", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    with open(dst, "rb") as fh:
        out_data = fh.read()
    if hashlib.sha256(out_data).hexdigest() != hashlib.sha256(data).hexdigest():
        print("output sha256 does not match entry.png", file=sys.stderr)
        return 1
    if len(out_data) > 1048576:
        print(f"output is {len(out_data)} bytes, over the 1 MiB cap", file=sys.stderr)
        return 1
    print(f"OK: wrote {dst} ({len(out_data)} bytes, 1024x1024, "
          f"sha256 {hashlib.sha256(out_data).hexdigest()[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
