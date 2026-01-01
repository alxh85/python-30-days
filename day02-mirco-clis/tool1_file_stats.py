import argparse
from pathlib import Path


def build_parser():
    parser = argparse.ArgumentParser(
        description="Count lines, words, and characters for one or more files"
    )

    parser.add_argument(
        "files",
        nargs="+",
        help="One or more file paths to analyze",
    )

    parser.add_argument(
        "--total",
        action="store_true",
        help="Print totals across all processed files",
    )

    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)

    total_lines = 0
    total_words = 0
    total_chars = 0
    processed = 0

    for file_arg in args.files:
        p = Path(file_arg)

        if not p.exists():
            print(f"File not found: {p}")
            continue
        if not p.is_file():
            print(f"Not a file: {p}")
            continue

        # Reset counts PER FILE
        lines = 0
        words = 0
        chars = 0

        try:
            with p.open("r", encoding="utf-8") as f:
                for line in f:
                    lines += 1
                    words += len(line.split())
                    chars += len(line)

        except PermissionError:
            print(f"Permission denied: {p}")
            continue
        except UnicodeDecodeError:
            print(f"Could not decode (not UTF-8): {p}")
            continue

        print(f"{p}: {lines} lines, {words} words, {chars} characters")

        processed += 1
        total_lines += lines
        total_words += words
        total_chars += chars

    if args.total and processed > 0:
        print(f"TOTAL: {total_lines} lines, {total_words} words, {total_chars} characters")


if __name__ == "__main__":
    main()
