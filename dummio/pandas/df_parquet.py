"""Pandas data frames to/from parquet."""

from typing import Any

import pandas as pd

from dummio.constants import PathType
from dummio.pandas.utils import add_storage_options

ENGINE = "engine"
PYARROW = "pyarrow"
FASTPARQUET = "fastparquet"


def save(
    data: pd.DataFrame,
    *,
    filepath: PathType,
    **kwargs: Any,
) -> None:
    """Save a data frame to a parquet file.

    If the user does not specify the parquet engine and the data contains a column named None, the engine will be set to
    "pyarrow" to avoid defaulting to "fastparquet" which does not support None column names.

    Args:
        data: Data to save.
        filepath: Path to save the data.
        **kwargs: Additional keyword arguments for pandas.DataFrame.to_parquet
    """
    add_storage_options(filepath=filepath, kwargs=kwargs)
    if None in data.columns:
        if ENGINE not in kwargs:
            kwargs[ENGINE] = PYARROW
    try:
        data.to_parquet(filepath, **kwargs)
    except TypeError as err:
        using_fastparquet = kwargs.get(ENGINE, "") == FASTPARQUET
        none_colname_err = "Column name must be a string" in str(err)
        if using_fastparquet and none_colname_err:
            msg = "specify engine='pyarrow', not 'fastparquet' if you really want to support None column names."
            raise ValueError(msg) from err
        raise err


def load(filepath: PathType, **kwargs: Any) -> pd.DataFrame:
    """Read a parquet file.

    Args:
        filepath: Path to read the data.
        **kwargs: Additional keyword arguments for pandas.read_parquet
    """
    add_storage_options(filepath=filepath, kwargs=kwargs)
    return pd.read_parquet(filepath, **kwargs)
