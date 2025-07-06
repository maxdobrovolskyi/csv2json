import pandas as pd
import os
import json

chunk_size = 100000
LARGE_FILE_THRESHOLD = 1 * 1024 * 1024 * 1024


def read(file, where: str = None):
    file_size = os.path.getsize(file)
    df = None
    if file_size >= LARGE_FILE_THRESHOLD:
        list_of_chunks = []
        df = pd.read_csv(file, chunksize=chunk_size)

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


def to_json(df):
    list_of_records = df.to_dict(orient="records")
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(list_of_records, f, ensure_ascii=False, indent=2)
