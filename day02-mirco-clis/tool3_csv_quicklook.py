import argparse
import csv
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    """
    Build and return the CLI argument parser.

    You should understand:
    - positional arguments (csv_path)
    - optional arguments (--head, --delimiter)
    - default values and type=int
    """
    parser = argparse.ArgumentParser(
        description="Quickly inspect a CSV file: columns, row count, missing %, and simple type inference."
    )
    parser.add_argument("csv_path", help="Path to the CSV file")
    parser.add_argument("--head", type=int, default=5, help="How many rows to preview (default: 5)")
    parser.add_argument("--delimiter", default=",", help="CSV delimiter (default: ,)")
    return parser


def is_missing(value: str) -> bool:
    """
    Return True if a value should be treated as missing.

    Definition for this project:
    - missing if the value is empty after stripping whitespace
      Examples: "" -> missing, "   " -> missing
    """
    return value.strip() == ""


def is_number(value: str) -> bool:
    """
    Return True if a string can be safely interpreted as a number.

    For this tool:
    - Treat numeric if float(value) works.
    - If float(...) raises ValueError, it's not numeric.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False


def main(argv=None) -> None:
    args = build_parser().parse_args(argv)

    # ===== Step 1: Validate arguments =====
    # TODO: validate args.head is >= 0
    # If invalid, exit nicely like:
    #   raise SystemExit("ERROR: --head must be >= 0")

    if args.head < 0:
        raise SystemExit("ERROR: --head must be >= 0")


    # ===== Step 2: Validate file path =====
    path = Path(args.csv_path)

    # TODO: check file exists, else SystemExit with a helpful error
    # TODO: check it's a file (not a folder), else SystemExit

    if not path.exists():
        raise SystemExit(f"ERROR: file not found: {path}")

    if not path.is_file():
        raise SystemExit(f"ERROR: not a file: {path}")


    row_count = 0
    preview_rows = []

    with path.open("r", encoding="utf-8", newline="") as f:
        # what does the "r" mean here?
        reader = csv.DictReader(f, delimiter=args.delimiter)

        if reader.fieldnames is None:
            raise SystemExit("ERROR: Could not read header row (no columns found).")

        columns = reader.fieldnames

        # Initialize stats dicts
        missing_counts = {c: 0 for c in columns}
        numeric_possible = {c: True for c in columns}   # stays True only if all non-missing values are numeric
        non_missing_seen = {c: 0 for c in columns}
        # why do we need the numeric_possible and non_missing_seen dicts?
        # explain how {c: 0 for c in columns} works

        for row in reader:
            row_count += 1

            # preview rows
            if len(preview_rows) < args.head:
                preview_rows.append(row)

            # per-column stats
            for c in columns:
                val = row.get(c, "")
                # why are we using row.get?
                # what does the second argument to get do?
                # what if we just did val = row[c]?
                val = "" if val is None else str(val)
                # what is this line doing?

                if is_missing(val):
                    missing_counts[c] += 1
                else:
                    non_missing_seen[c] += 1
                    if numeric_possible[c] and not is_number(val.strip()):
                        numeric_possible[c] = False



                





    # ===== Step 4: Print summary =====
    # After processing:
    # Print:
    # - File path
    # - Total row count
    # - Column names
    #
    # Then for each column:
    # - missing count and missing %
    # - inferred type:
    #     - "empty" if non_missing_seen[col] == 0
    #     - "numeric" if numeric_possible[col] is True
    #     - "text" otherwise

    print(f"File: {path}")
    print(f"Rows: {row_count}")
    print(f"Columns ({len(columns)}): {', '.join(columns)}")
    print()

    print("Column summary:")
    for c in columns:
        miss = missing_counts[c]
        miss_pct = (miss / row_count * 100) if row_count > 0 else 0.0

        if non_missing_seen[c] == 0:
            col_type = "empty"
        else:
            col_type = "numeric" if numeric_possible[c] else "text"

        print(f"- {c}: type={col_type}, missing={miss} ({miss_pct:.1f}%)")


    # ===== Step 5: Print preview =====
    # Print the first N rows you captured.
    # Keep it simple: print the row dicts. (Later you can format prettier.)

    # NOTE: If row_count is 0, handle missing % without dividing by zero.

    print()
    print(f"Preview (first {min(args.head, len(preview_rows))} rows):")
    for i, row in enumerate(preview_rows, start=1):
        print(f"{i}. {row}")


if __name__ == "__main__":
    main()



