import pandas as pd
import argparse
from pathlib import Path

# This requires python version >= 3.9

def xlsx_to_csv(file: str) -> str:
    """Takes a valid filepath, converts the xlsx document to csv
       returns a string of that new file path."""
    p = Path(file)
    if p.suffix.lower() != ".xlsx":
        raise ValueError(f"Expected .xlsx file, got: {p}")
    read_file = pd.read_excel(file)
    res = read_file.to_csv(p.with_suffix(".csv"), index=None, header=True)
    return res


def main():
    """Takes arguments and converts files"""
    parser = argparse.ArgumentParser(
        description="Add file paths to be processed"
    )

    parser.add_argument("-f", "--files", type=str, nargs="+", help="One or more space seperated filepaths XLSX ONLY")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    if (args.verbose):
        print(f"Total files provided: {len(args.files)}")
        print(f"File list: {args.files}")

    new_files: list[str] = []

    for i, file in enumerate(args.files, 1):
        res = xlsx_to_csv(file)
        new_files.append(res)

    if (args.verbose):
        print(f"\nTotal files converted: {len(args.files)}")
        print(f"File list: {args.files}")


if __name__ == "__main__":
    main()
