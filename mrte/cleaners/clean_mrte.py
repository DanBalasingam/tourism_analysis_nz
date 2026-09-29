import argparse
from pathlib import Path

import pandas as pd

import clean

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
_RAW_DIR = _DATA_DIR / "raw"
_OUTPUT_DIR = _DATA_DIR / "cleaned"

def clean_mrte(path: str, level: str) -> pd.DataFrame:
    df = clean.load(path, sheet="Data base")

    df = df.rename(columns={df.columns[1]: "area"})

    df = clean.normalise_text(df)

    spend = [c for c in df.columns if c.endswith("_spend")]
    df[spend] = df[spend].clip(lower=0)

    df["month"] = df.pop("date").dt.to_period("M")
    for c in ["area", "product", "visitor_type", "origin"]:
        df[c] = df[c].astype("category")

    if "monthly_spend" not in df.columns:
        df["monthly_spend"] = pd.NA

    key = ["month", "area", "product", "visitor_type", "origin"]
    assert not df.duplicated(key).any(), "duplicate keys"
    assert df[key].notna().all().all(), "null in key column"

    df["level"] = level
    return df[["level", *key, "annual_spend", "monthly_spend"]]


def main():
    parser = argparse.ArgumentParser(
        description="Clean MRTE xlsx worksheets, allows for output of .parquet (recommended) or .xlsx"
    )

    parser.add_argument("--xlsx", action="store_true", help="Outputs a .xlsx file.")
    parser.add_argument("--parquet", action="store_true", help="Outputs a parquet file.")

    args = parser.parse_args()

    if not args.xlsx:
        args.parquet = True

    files = {"ta": f"{_RAW_DIR}/TA-series.xlsx", "region": f"{_RAW_DIR}/Region-series.xlsx", "rto": f"{_RAW_DIR}/RTO-series.xlsx"}
    data = {level: clean_mrte(f, level) for level, f in files.items()}

    totals = pd.DataFrame({k: v.groupby("month")["annual_spend"].sum() for k, v in data.items()})
    assert (totals.sub(totals["region"], axis=0).abs() < 1e-6).all().all()

    if (args.xlsx):
        with pd.ExcelWriter(f"{_OUTPUT_DIR}/mrte_clean.xlsx", engine="xlsxwriter") as writer:
            for lvl, df in data.items():
                out = df.copy()
                out["month"] = out["month"].dt.to_timestamp()
                out.to_excel(writer, sheet_name=lvl.upper(), index=False)

    if (args.parquet):
        for lvl, df in data.items():
            df.to_parquet(f"{_OUTPUT_DIR}/mrte_{lvl}.parquet")


if __name__ == "__main__":
    main()
