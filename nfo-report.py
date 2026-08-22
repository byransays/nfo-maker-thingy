#!/usr/bin/env python3
"""Report which media files have no NFO sitting alongside them."""

import argparse
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="List media files that have no matching .nfo file."
    )
    parser.add_argument("files", nargs="+", help="Media file(s) to check")
    parser.add_argument(
        "-c",
        "--count",
        action="store_true",
        help="Print just the number missing, for tracking progress between runs",
    )
    args = parser.parse_args()

    missing = []
    checked = 0
    for name in args.files:
        path = Path(name)
        # Tolerate a bare "*" glob: an NFO is not itself missing an NFO.
        if path.suffix.lower() == ".nfo":
            continue
        checked += 1
        if not path.with_suffix(".nfo").exists():
            missing.append(path)

    if args.count:
        print(len(missing))
        return

    for path in missing:
        print(path)

    # Summary on stderr so stdout stays clean for piping into xargs.
    print(
        f"{len(missing)} of {checked} missing an NFO "
        f"({checked - len(missing)} present)",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
