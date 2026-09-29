# tourism_analysis_nz

Basic use of Data Cleaning and Validating using Python.

## Layout

```
packages/clean/        Reusable cleaning/validation library (installable package)
  pyproject.toml
  src/clean/           load, normalise_text, convert_types, profile, xlsx_to_csv, read_file
mrte/                  Monthly Regional Tourism Estimates workspace
  requirements.txt     pinned deps + editable install of ../packages/clean
  venv/                the workspace virtualenv (see the note below)
  data/raw/            source .xlsx workbooks (do not edit)
  data/cleaned/        cleaner output (.parquet / .xlsx / .csv)
  cleaners/            scripts that turn raw into cleaned
```

## Setup

Create the venv for the MRTE workspace and install its requirements. This also
installs `clean` in editable mode, so edits to the library take effect
immediately. Run pip from `mrte/` — the `-e ../packages/clean` line in
`requirements.txt` is relative to the working directory.

```
cd mrte
python3 -m venv venv
```

- (Linux/macOS) `./venv/bin/python -m pip install -r requirements.txt`
- (Windows) `.\venv\Scripts\python -m pip install -r requirements.txt`

(alternatively you can activate a venv session then run `pip install -r ...`)

### Why `venv/` and not `.venv/`

On macOS, dot-prefixed paths can pick up the `UF_HIDDEN` file flag, and
everything inside them inherits it. Python 3.14's `site` module silently skips
any `.pth` file carrying that flag (`site.py`, `addpackage`), which breaks
editable installs with no error at all — `import clean` just fails with
`ModuleNotFoundError` minutes after a working install. A venv directory without
the leading dot avoids the flag entirely. If you do hit it, clear it with:

```
chflags nohidden venv/lib/python3.14/site-packages/*.pth
```

## Running the cleaners

From `mrte/` (the scripts resolve `data/` relative to their own location, so the
working directory does not matter):

```
./venv/bin/python cleaners/clean_mrte.py            # defaults to parquet
./venv/bin/python cleaners/clean_mrte.py --xlsx
./venv/bin/python cleaners/summary_clean.py
```
