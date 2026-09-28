import argparse
from pathlib import Path
# Looks through data and identifies variables, missing values, duplicates

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



if __name__ == "__main__":
    main()
