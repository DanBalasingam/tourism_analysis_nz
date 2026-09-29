"""
Main file in this project.

Works out of the 3 Main MRTE excel sheets.

Cleans, formats, validates and merges all datasheets.
"""
import pandas as pd
from pathlib import Path
import numpy as np

NULL_TOKENS: list[str] = ["", "-", "n/a", "na", "null", "unknown", "?"]

def load(path: str, sheet: str) -> pd.DataFrame:
    """Reads xlsx sheet and returns a pandas data frame.
        Cleans whitespace and converts to snake_case"""
    df = pd.read_excel(path, sheet_name=sheet)
    df.columns = df.columns.str.strip().str.lower().str.replace(r"\W+", "_", regex=True)
    return df


def normalise_text(df: pd.DataFrame) -> pd.DataFrame:
    """Foreach column in data strip whitespcae,
        replace NULL_TOKENS with NaN, returns data frame."""
    for col in df.select_dtypes("object"):
        df[col] = df[col].str.strip()
        df.loc[df[col].str.lower().isin(NULL_TOKENS), col] = np.nan

    return df


def convert_types(df: pd.DataFrame, date_cols: tuple=(), num_cols: tuple=()) -> pd.DataFrame:
    """Foreach date in data convert to proper datetime.
        Foreach number convert to proper numric."""
    for col in date_cols:
        before = df[col].notna().sum()
        df[col] = pd.to_datetime(df[col], errors="coerce")
        print(f"{col}: {before - df[col].notna().sum()} unparseable dates...")

    for col in num_cols:
        df[col] = pd.to_numric(df[col], errors="coerce")

    return df


def profile(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "dtype": df.dtypes,
        "null_pct": df.isna().mean().round(3) * 100,
        "unique": df.nunique(),
    })
