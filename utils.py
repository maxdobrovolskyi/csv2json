from __future__ import annotations
import pandas as pd
import os
import json
import yaml
import sys
import config


def transform(yaml_file: str, df: pd.DataFrame) -> pd.DataFrame:
    with open(yaml_file, "r", encoding="utf-8") as f:
        try:
            column_rename = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(e)
    return df.rename(columns=column_rename)


def extract(df: pd.DataFrame, file_name: str | None, pretty: bool) -> None:
    list_of_records = df.to_dict(orient="records")
    level = 2 if pretty else 0
    if file_name:
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(list_of_records, f, ensure_ascii=False, indent=level)
    else:
        json.dump(list_of_records, sys.stdout, ensure_ascii=False, indent=level)
        sys.stdout.write("\n")


def load(file: str, dates: str, where: str = None) -> pd.DataFrame:
    file_size = os.path.getsize(file)
    df = None
    if file_size >= config.LARGE_FILE_THRESHOLD:
        list_of_chunks = []
        if dates:
            df = pd.read_csv(file, chunksize=config.CHUNK_SIZE, parse_dates=[dates])
        else:
            df = pd.read_csv(file, chunksize=config.CHUNK_SIZE)
        for chunk in df:
            if where:
                filtered_query = chunk.query(where)
                list_of_chunks.append(filtered_query)
            else:
                list_of_chunks.append(chunk)

        df = pd.concat(list_of_chunks, ignore_index=True)
    else:
        if dates:
            df = pd.read_csv(file, parse_dates=[dates])
        else:
            df = pd.read_csv(file)
        if where:
            df = df.query(where)
    return df
