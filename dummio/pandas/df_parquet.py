"""Pandas data frames to/from parquet."""

from typing import Any

import pandas as pd

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
        **kwargs: Additional keyword arguments for pandas.DataFrame.to_parquet
    """
    add_storage_options(filepath=filepath, kwargs=kwargs)
    data.to_parquet(filepath, **kwargs)


def load(filepath: PathType, **kwargs: Any) -> pd.DataFrame:
    """Read a parquet file.

    Args:
        filepath: Path to read the data.
        **kwargs: Additional keyword arguments for pandas.read_parquet
    """
    add_storage_options(filepath=filepath, kwargs=kwargs)
    return pd.read_parquet(filepath, **kwargs)
