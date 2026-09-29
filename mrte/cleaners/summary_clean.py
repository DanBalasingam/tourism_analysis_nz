import pandas as pd
from pathlib import Path

# Cleans the Summary.xlsx file

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"

COLUMNS = [
    "month_dom_spend", "month_intl_spend",
    "month_dom_pct_1y", "month_intl_pct_1y",
    "month_dom_pct_2y", "month_intl_pct_2y",
    "annual_dom_spend", "annual_intl_spend",
    "annual_dom_pct_1y", "annual_intl_pct_1y",
    "annual_dom_pct_2y", "annual_intl_pct_2y",
]


def load_mtre_summary(path: str) -> pd.DataFrame:
    raw = pd.read_excel(path, header=None)

    first_col = raw.iloc[:, 0].astype(str).str.strip()
    header_idx = first_col[first_col == "REGION"].index[0]

    df = raw.iloc[header_idx + 1:]
    df = df.dropna(axis=1, how="all").dropna(axis=0, how="all")
    df = df.set_index(df.columns[0])
    df.index.name = "region"

    if len(df.columns) != len(COLUMNS):
        raise ValueError(f"Expected {len(COLUMNS)} columns, got {len(df.columns)}")
    df.columns = COLUMNS

    return df.apply(pd.to_numeric)


def export_csv(df: pd.DataFrame, source: str | Path) -> Path:
    out = _DATA_DIR / "cleaned" / Path(source).with_suffix(".csv").name
    df.to_csv(out, index=True, float_format="%.4f", encoding="utf-8")
    return out


if __name__ == "__main__":
    src = _DATA_DIR / "raw" / "Summary.xlsx"
    df = load_mtre_summary(src)
    export_csv(df, src)
