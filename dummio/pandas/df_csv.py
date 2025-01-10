"""Pandas data frames to/from csv."""

from typing import Any

import pandas as pd
from pandahandler.indexes import is_unnamed_range_index

from dummio.constants import PathType
from dummio.pandas.utils import add_storage_options


def save(
    data: pd.DataFrame,
    *,
    filepath: PathType,
    **kwargs: Any,
) -> None:
    """Save a parquet file.

    Args:
        data: Data to save.
        filepath: Path to save the data.
        **kwargs: Additional keyword arguments for pandas.DataFrame.to_csv
    """
    if "index" not in kwargs and is_unnamed_range_index(data.index):
        kwargs["index"] = False
    add_storage_options(filepath=filepath, kwargs=kwargs)
    data.to_csv(filepath, **kwargs)


def load(filepath: PathType, **kwargs: Any) -> pd.DataFrame:
    """Read a parquet file.

    Args:
        filepath: Path to read the data.
        **kwargs: Additional keyword arguments for pandas.read_csv
    """
    add_storage_options(filepath=filepath, kwargs=kwargs)
    return pd.read_csv(filepath, **kwargs)
