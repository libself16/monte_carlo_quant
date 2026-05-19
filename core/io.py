from pathlib import Path
from typing import Optional

import pandas as pd


def load_trade_data(config):
    source = Path(config.INPUT_FOLDER)
    if not source.exists():
        raise FileNotFoundError(f"Input folder not found: {source}")

    if config.INPUT_FILE:
        sources = [source / config.INPUT_FILE]
    else:
        sources = sorted(source.glob("*.csv")) + sorted(source.glob("*.xls*"))

    frames = []
    for path in sources:
        if not path.exists():
            continue
        if path.suffix.lower() == ".csv":
            df = pd.read_csv(path)
        else:
            df = pd.read_excel(path)
        frames.append(df)

    if not frames:
        raise FileNotFoundError(f"No input files found in {source}")

    df = pd.concat(frames, ignore_index=True)
    columns = {config.CSV_COLUMNS["symbol"]: "Symbol", config.CSV_COLUMNS["return"]: "R"}
    df = df.rename(columns={k: v for k, v in columns.items() if k in df.columns})

    if "Symbol" not in df.columns or "R" not in df.columns:
        raise ValueError("Input data must contain 'Symbol' and 'R' columns.")

    df["Symbol"] = df["Symbol"].astype(str).str.strip()
    df["R"] = pd.to_numeric(df["R"], errors="coerce")
    df = df.dropna(subset=["Symbol", "R"])

    if config.SYMBOL_FILTER:
        if isinstance(config.SYMBOL_FILTER, str):
            allowed = [config.SYMBOL_FILTER]
        else:
            allowed = list(config.SYMBOL_FILTER)
        df = df[df["Symbol"].isin(allowed)]

    if df.empty:
        raise ValueError("No trade data available after applying filters.")

    return df.reset_index(drop=True)
