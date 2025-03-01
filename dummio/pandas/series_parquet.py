"""Pandas series to/from parquet.

Built-in pandas.Series "to_[filetype]" methods (excluding pickle) generally don't preserve data types as rigorously as
parquet does.
"""

import warnings
from typing import Any

import pandas as pd

from dummio.constants import PathType
from dummio.pandas import df_parquet


def save(
    data: pd.Series,
    *,
    filepath: PathType,
    **kwargs: Any,
) -> None:
    """Save a series to a parquet file.

    Args:
        data: Data to save.
        filepath: Path to save the data.
        **kwargs: Additional keyword arguments for pandas.DataFrame.to_parquet
    """
    df = data.to_frame()
    # in case data.name is None, to_frame (above) imputes df.columns[0] as "0", which is not desired in this context:
    if data.name is None:
        df.columns = [data.name]
        # ignore "*** UserWarning: The DataFrame has column names of mixed type. They will be converted to strings and
        # not roundtrip correctly."
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message=".*mixed type.*roundtrip.*")
            df_parquet.save(df, filepath=filepath, **kwargs)
    else:
        df_parquet.save(df, filepath=filepath, **kwargs)


def load(filepath: PathType, **kwargs: Any) -> pd.Series:
    """Read a parquet file as a pandas series.

    Args:
        filepath: Path to read the data.
        **kwargs: Additional keyword arguments for pandas.read_parquet

    Raises:
        RuntimeError: if the loaded data has more than one column, indicating that it should be read with `df_parquet`
          instead of `series_parquet`.
        RuntimeError: if the loaded data has no columns, making it impossible to construct a series.
    """
    df = df_parquet.load(filepath, **kwargs)
    n_cols = df.shape[1]
    if n_cols > 1:
        msg = "Loaded data has more than one column. Use `from dummio.pandas.df_parquet import load` instead."
        raise RuntimeError(msg)
    if n_cols < 1:
        raise RuntimeError("No columns loaded.")
    series = df.squeeze()
    assert isinstance(series, pd.Series), "expected a pandas series since df has exactly one column"
    return series
