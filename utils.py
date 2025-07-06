from __future__ import annotations
import pandas as pd
import os
import json
import yaml
import sys


chunk_size = 100000
LARGE_FILE_THRESHOLD = 1 * 1024 * 1024 * 1024


def transform(yaml_file: str, df: pd.DataFrame) -> pd.DataFrame:
    with open(yaml_file, "r", encoding="utf-8") as f:
        columl_rename = yaml.safe_load(f)
    return df.rename(columns=columl_rename)


def extract(df: pd.DataFrame, file_name: str | None, pretty: bool) -> None:
    list_of_records = df.to_dict(orient="records")
    level = 2 if pretty else 0
    if file_name:
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(list_of_records, f, ensure_ascii=False, indent=level)
    else:
        json.dump(list_of_records, sys.stdout, ensure_ascii=False, indent=level)
        sys.stdout.write("\n")


def load(file: str, where: str = None) -> pd.DataFrame:
    file_size = os.path.getsize(file)
    df = None
    if file_size >= LARGE_FILE_THRESHOLD:
        list_of_chunks = []
        df = pd.read_csv(file, chunksize=chunk_size, parse_dates=["date"])

        for chunk in df:
            if where:
                filtered_query = chunk.query(where)
                list_of_chunks.append(filtered_query)
            else:
                list_of_chunks.append(chunk)

        df = pd.concat(list_of_chunks, ignore_index=True)
        if where:
            df = df.query(where)
    else:
        df = pd.read_csv(file)
        if where:
            df = df.query(where)
    return df
