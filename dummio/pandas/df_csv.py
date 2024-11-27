"""Pandas data frames to/from csv."""

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
        **kwargs: Additional keyword arguments for pandas.DataFrame.to_csv
    """
    if "index" not in kwargs and not data.index.name:
        kwargs["index"] = False
    data.to_csv(filepath, **kwargs)


def load(filepath: PathType, **kwargs: Any) -> pd.DataFrame:
    """Read a yaml file.

    Args:
        filepath: Path to read the data.
        **kwargs: Additional keyword arguments for pandas.read_csv
    """
    return pd.read_csv(filepath, **kwargs)
