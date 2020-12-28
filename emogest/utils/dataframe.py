from typing import List

import pandas as pd


def create_dataframe(columns: List[str] = None) -> pd.DataFrame:
    if columns == None:
        return pd.DataFrame()

    return pd.DataFrame(columns=columns)


def append_row(df: pd.DataFrame, rows: dict) -> pd.DataFrame:
    _df = pd.DataFrame(rows)
    appended_df = df.append(_df, ignore_index=True)

    return appended_df


def dump_dataframe(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False)
