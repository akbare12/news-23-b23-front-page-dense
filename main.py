#!/usr/bin/env python3
"""news-23 b23 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only. Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import os
import struct
import sys

MAX_BYTES = 1024 * 1024


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    with open(src, "rb") as f:
        data = f.read()

    # --- validate the PNG header by hand (no image library) ---
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        print("error: not a PNG file", file=sys.stderr)
        return 1
    # first chunk must be IHDR, 13 bytes, 1024x1024
    length, ctype = struct.unpack(">I4s", data[8:16])
    if ctype != b"IHDR" or length != 13:
        print("error: bad IHDR chunk", file=sys.stderr)
        return 1
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        print(f"error: expected 1024x1024, got {width}x{height}",
              file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print(f"error: entry.png is {len(data)} bytes (> 1 MiB)",
              file=sys.stderr)
        return 1
    # last chunk must be a well-formed IEND trailer (12 bytes: len 0 + IEND + CRC)
    if len(data) < 12 or data[-12:-8] != b"\x00\x00\x00\x00" \
            or data[-8:-4] != b"IEND":
        print("error: missing or malformed IEND trailer", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    # guard: never write into the repo itself, even if the env var is odd
    if os.path.abspath(out_dir) == here:
        print("error: MAKEFUN_OUTPUT_DIR must not be the repo dir",
              file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    # re-read the output and confirm it is byte-identical to the source
    with open(dst, "rb") as f:
        written = f.read()
    if written != data:
        print("error: output differs from entry.png", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({len(data)} bytes, 1024x1024)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
