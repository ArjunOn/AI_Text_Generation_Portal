"""Simple data preprocessing utilities for the project.

This module provides a small, dependency-light preprocessing script that:
- Loads the CSV produced by the WebScraping scraper (default: ../WebScraping/country_data.csv)
- Normalizes textual fields (lowercase, strip)
- Normalizes numeric fields (remove commas, cast to int when possible)
- Writes a cleaned CSV to datapreprocessing/processed_country_data.csv

Usage:
    python preprocess.py --input ../WebScraping/country_data.csv --output processed_country_data.csv

The script uses pandas which is already a dependency of the project.
"""
from __future__ import annotations

import argparse
import os
import re
from typing import Optional

import pandas as pd

NUMERIC_RE = re.compile(r"[\d,]+")


def clean_text(value: Optional[str]) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    # basic normalization
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = ' '.join(text.split())
    return text


def parse_int(value: Optional[str]) -> Optional[int]:
    if value is None:
        return None
    s = str(value).strip()
    if s == "":
        return None
    # remove commas and non-digit characters
    m = NUMERIC_RE.search(s)
    if not m:
        return None
    digits = m.group(0).replace(',', '')
    try:
        return int(digits)
    except ValueError:
        return None


def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    # Normalize Name and Capital
    for col in ["Name", "Capital"]:
        if col in out.columns:
            out[col] = out[col].apply(clean_text).str.lower()

    # Normalize Population and Area
    for col in ["Population", "Area"]:
        if col in out.columns:
            out[col + "_clean"] = out[col].apply(parse_int)

    return out


def main(input_path: str, output_path: str) -> None:
    if not os.path.exists(input_path):
        print(f"Input file not found: {input_path}")
        return

    df = pd.read_csv(input_path)
    cleaned = preprocess_df(df)
    cleaned.to_csv(output_path, index=False)
    print(f"Wrote cleaned data to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", default="../WebScraping/country_data.csv", help="Path to input CSV")
    parser.add_argument("--output", "-o", default="processed_country_data.csv", help="Path to output CSV")
    args = parser.parse_args()
    main(args.input, args.output)
