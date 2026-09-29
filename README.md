# tourism_analysis_nz

Basic use of Data Cleaning and Validating using Python.

## Layout

```
packages/clean/        Reusable cleaning/validation library (installable package)
  pyproject.toml
  src/clean/           load, normalise_text, convert_types, profile, xlsx_to_csv, read_file
mrte/                  Monthly Regional Tourism Estimates workspace
  requirements.txt     pinned deps + editable install of ../packages/clean
  data/raw/            source .xlsx workbooks (do not edit)
  data/cleaned/        cleaner output (.parquet / .xlsx / .csv)
  cleaners/            scripts that turn raw into cleaned
```

## Setup

Create the venv for the MRTE workspace and install its requirements. This also
installs `clean` in editable mode, so edits to the library take effect
immediately. Run it from `mrte/` — the `-e ../packages/clean` line in
`requirements.txt` is relative to the working directory.

```
cd mrte
python3 -m venv .venv
```

- (Linux/macOS) `./.venv/bin/python -m pip install -r requirements.txt`
- (Windows) `.\.venv\Scripts\python -m pip install -r requirements.txt`

(alternatively you can activate a .venv session then run `pip install -r ...`)

For the `.xlsx` / `.parquet` writers used by `clean_mrte.py`, also install the
export extras:

```
./.venv/bin/python -m pip install -e "../packages/clean[export]"
```

## Running the cleaners

From `mrte/` (the scripts resolve `data/` relative to their own location, so the
working directory does not matter):

```
./.venv/bin/python cleaners/clean_mrte.py --parquet
./.venv/bin/python cleaners/summary_clean.py
```
