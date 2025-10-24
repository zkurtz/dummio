"""Pandas data frames to/from vortex."""

from typing import Any

import pandas as pd
import pyarrow as pa
import vortex
import vortex.io

from dummio.constants import PathType


def save(
    data: pd.DataFrame,
    *,
    filepath: PathType,
    **kwargs: Any,
) -> None:
    """Save a data frame to a vortex file.

    Args:
        data: Data to save.
        filepath: Path to save the data.
        **kwargs: Additional keyword arguments for vortex.io.write
    """
    # Convert DataFrame to Arrow table and write to file
    table = pa.Table.from_pandas(data)
    vortex.io.write(table, str(filepath), **kwargs)


def load(filepath: PathType, **kwargs: Any) -> pd.DataFrame:
    """Read a vortex file.

    Args:
        filepath: Path to read the data.
        **kwargs: Additional keyword arguments (currently unused)

    Returns:
        DataFrame: The loaded pandas DataFrame
    """
    # Open the vortex file
    vortex_file = vortex.open(str(filepath))

    # Convert to Arrow RecordBatchReader, then to table, then to pandas
    arrow_reader = vortex_file.to_arrow()
    table = arrow_reader.read_all()

    return table.to_pandas()
