"""Pandas data frames to/from csv."""

from typing import Any

import pandas as pd
from upath import UPath

from dummio.constants import PathType


def save(
    data: pd.DataFrame,
    *,
    filepath: PathType,
    **kwargs: Any,
) -> None:
    """Save a feather file.

    Args:
        data: Data to save.
        filepath: Path to save the data.
        **kwargs: Additional keyword arguments for pandas.DataFrame.to_feather
    """
    with UPath(filepath).open("wb") as file:
        data.to_feather(file, **kwargs)


def load(filepath: PathType, **kwargs: Any) -> pd.DataFrame:
    """Read a feather file.

    Args:
        filepath: Path to read the data.
        **kwargs: Additional keyword arguments for pandas.read_feather
    """
    with UPath(filepath).open("rb") as file:
        return pd.read_feather(file, **kwargs)
