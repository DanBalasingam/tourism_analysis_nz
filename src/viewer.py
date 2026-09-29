import argparse
from pathlib import Path
from typing import Any
import pandas as pd

# Looks through data for output

def read_file(filepath: str) -> list[Any]:
    """Takes a file, reads it, returns a list"""
    return pd.read_csv(filepath)


def main():
    parser = argparse.ArgumentParser(
        description="Add file paths to be processed"
    )

    parser.add_argument("-f", "--files", type=str, nargs="+", help="One or more space seperated filepaths CSV ONLY")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    if (args.verbose):
        print(f"Total files provided: {len(args.files)}")
        print(f"File list: {args.files}")

    for i, file in enumerate(args.files, 1):
        p = Path(file)
        if p.suffix.lower() != ".csv":
            raise ValueError(f"Expected .csv file(s), got: {p}")
        content = read_file(file)
        print(content)


if __name__ == "__main__":
    main()
