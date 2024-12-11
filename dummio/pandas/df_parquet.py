"""Pandas data frames to/from parquet."""

from typing import Any

import pandas as pd
from upath import UPath

from dummio.constants import PathType

STORAGE_OPTIONS = "storage_options"


def add_storage_options(*, filepath: PathType, kwargs: dict[str, Any]) -> None:
    """If filepath is a universal path, make sure that kwargs includes storage options."""
    if isinstance(filepath, UPath):
        if STORAGE_OPTIONS not in kwargs:
            kwargs[STORAGE_OPTIONS] = dict(filepath.storage_options)


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
    add_storage_options(filepath=filepath, kwargs=kwargs)
    data.to_parquet(filepath, **kwargs)


def load(filepath: PathType, **kwargs: Any) -> pd.DataFrame:
    """Read a yaml file.

    Args:
        filepath: Path to read the data.
        **kwargs: Additional keyword arguments for pandas.read_parquet
    """
    add_storage_options(filepath=filepath, kwargs=kwargs)
    return pd.read_parquet(filepath, **kwargs)
