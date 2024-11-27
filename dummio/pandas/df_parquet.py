"""Pandas data frames to/from parquet."""

from typing import Any

import pandas as pd

from dummio.constants import PathType


def save(
    data: pd.DataFrame,
    *,
    filepath: PathType,
    **kwargs: Any,
) -> None:
    """Save a yaml file.

    Args:
        data: Data to save.
        filepath: Path to save the data.
        **kwargs: Additional keyword arguments for pandas.DataFrame.to_parquet
    """
    data.to_parquet(filepath, **kwargs)


def load(filepath: PathType, **kwargs: Any) -> pd.DataFrame:
    """Read a yaml file.

    Args:
        filepath: Path to read the data.
        **kwargs: Additional keyword arguments for pandas.read_parquet
    """
    return pd.read_parquet(filepath, **kwargs)
