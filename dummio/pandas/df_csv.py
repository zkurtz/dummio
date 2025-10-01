"""Pandas data frames to/from csv."""

from typing import Any

import pandas as pd
from pandahandler.indexes import is_unnamed_range_index
from upath import UPath

from dummio.constants import PathType


def save(
    data: pd.DataFrame,
    *,
    filepath: PathType,
    **kwargs: Any,
) -> None:
    """Save a csv file.

    Args:
        data: Data to save.
        filepath: Path to save the data.
        **kwargs: Additional keyword arguments for pandas.DataFrame.to_csv
    """
    if "index" not in kwargs and is_unnamed_range_index(data.index):
        kwargs["index"] = False
    with UPath(filepath).open("wb") as file:
        data.to_csv(file, **kwargs)


def load(filepath: PathType, **kwargs: Any) -> pd.DataFrame:
    """Read a csv file.

    Args:
        filepath: Path to read the data.
        **kwargs: Additional keyword arguments for pandas.read_csv
    """
    with UPath(filepath).open("rb") as file:
        return pd.read_csv(file, **kwargs)
