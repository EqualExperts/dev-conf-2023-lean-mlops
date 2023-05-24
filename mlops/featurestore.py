from dataclasses import dataclass
import datetime as dt
import duckdb
import os

__duck_db_conn : duckdb.DuckDBPyConnection = duckdb.connect(os.getenv("DUCK_DB_DWH", "data_local/feature_store.duckdb"))


def duck_db_conn()->duckdb.DuckDBPyConnection:
    if not __duck_db_conn:
        raise ValueError("No duck DB connection")
    else:
        return __duck_db_conn




@dataclass
class FeatureSet:
    name: str
    as_of: dt.datetime
    location: str
    contents_hash: str


def get_dataset(location):
    ...

