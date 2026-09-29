import argparse
from pathlib import Path
from typing import Any
import pandas as pd

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


def read_file(filepath: str) -> list[Any]:
    """Takes a file, reads it, returns a list"""
    return pd.read_csv(filepath)


def main():
    parser = argparse.ArgumentParser(
        description="Add file paths to be processed"
    )

    parser.add_argument("-f", "--files", type=str, nargs="+", help="One or more space seperated filepaths CSV ONLY")
    parser.add_argument("--convert", action="store_true", help="Runs the convert to csv from xlsx command")
    parser.add_argument("--view", action="store_true", help="Runs the viewer command")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    if (args.verbose):
        print(f"Total files provided: {len(args.files)}")
        print(f"File list: {args.files}")

    if (args.convert):
        new_files: list[str] = []
        for i, file in enumerate(args.files, 1):
            res = xlsx_to_csv(file)
            new_files.append(res)

        if (args.verbose):
            print(f"\nTotal files converted: {len(args.files)}")
            print(f"File list: {args.files}")

    if (args.view):
        for i, file in enumerate(args.files, 1):
            p = Path(file)
            if p.suffix.lower() != ".csv":
                raise ValueError(f"Expected .csv file(s), got: {p}")
            content = read_file(file)
            print(content)

if __name__ == "__main__":
    main()
