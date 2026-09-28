from typing import Any
import pandas as pd

def read_file(filepath: str) -> list[Any]:
    """Takes a file, reads it, returns a list"""
    return pd.read_csv(filepath)
