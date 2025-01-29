"""Generic pandas data frame IO methods, supporting multiple file formats.

These save/load methods support file format inference based on the file extension as
proposed in https://github.com/pandas-dev/pandas/issues/60786.

Direct usage of native pandas data frame IO methods requires users to:
- Remember multiple method names for the various file formats (to_csv, read_parquet, etc.)
- Change code when switching formats

A unified `save`/`load` API simplifies common IO operations while maintaining explicit control when needed:
- format is inferred from the filepath extension, but a `format` arg can be passed to be explicit, raising an error in
    some cases where the inferred file type disagrees with passed file type.
- Both methods accept `**kwargs` and pass them along to the underlying file-type-specific pandas IO methods.
- We support some basic translation across discrepancies in arg names in existing IO methods (i.e.
     "usecols" in `read_csv` vs "columns" in `read_parquet`).

Examples:
```
df = ...

# Simplest happy path:
save(df, filepath='data.csv')  # Uses to_csv
df = load('data.parquet')  # Uses read_parquet

# Optionally, be explicit about expected file type
save(df, filepath='data.csv', format="csv")  # Uses to_csv
df = load('data.parquet', format="parquet")  # Uses read_parquet

# Raises ValueError for conflicting format info:
save(df, filepath='data.csv', format='parquet')  # Conflicting types
save(df, filepath='data.txt', format='csv')  # .txt implies text format

# Reading allows overrides for misnamed files:
df = load('mislabeled.txt', format='parquet')

# Support `save` when inferred format is missing or not a standard type:
save(df, filepath='data', format='csv')  # No extension, needs type
save(df, filepath='mydata.unknown', format='csv')  # Unclear extension
"""

import importlib
from dataclasses import dataclass
from typing import Callable

import pandas as pd
from upath import UPath

from dummio.constants import PathType

CSV = "csv"
FEATHER = "feather"
PARQUET = "parquet"
SUPPORTED_FORMATS = [CSV, FEATHER, PARQUET]


@dataclass
class Format:
    """Represent a file format and its corresponding pandas IO method names."""

    name: str

    @property
    def save_method(self) -> Callable:
        """The save method name."""
        if self.name not in SUPPORTED_FORMATS:
            raise RuntimeError(f"Unsupported format '{self.name}'")
        module = importlib.import_module(f"dummio.pandas.df_{self.name}")
        return module.save

    @property
    def load_method(self) -> Callable:
        """The load method name."""
        if self.name not in SUPPORTED_FORMATS:
            raise RuntimeError(f"Unsupported format '{self.name}'")
        module = importlib.import_module(f"dummio.pandas.df_{self.name}")
        return module.load


def _infer_format(filepath: PathType) -> Format | None:
    """Infer the file format based on the file extension."""
    extension = UPath(filepath).suffix.lstrip(".").lower()
    if not extension:
        return None
    return Format(name=extension)


def _resolve_format(
    *,
    filepath: PathType,
    input_format: str | None,
    allow_conflict: bool = False,
) -> Format:
    """Identify the format based on the filepath and/or format argument.

    Args:
        filepath: The file path.
        input_format: The format provided by the user.
        allow_conflict: If false (default), raise an error when the inferred and provided formats explicitly conflict.
            This is not applicable if input_format is None.
    """
    inferred_format = _infer_format(filepath)
    provided_format = Format(input_format) if input_format else None
    format = provided_format or inferred_format
    if not format:
        raise ValueError("File format could not be inferred from the file extension and `format` was not provided.")
    if format.name not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported format '{format.name}'")
    if provided_format and inferred_format and not allow_conflict:
        if provided_format != inferred_format:
            raise ValueError(
                f"Conflicting format information: inferred '{inferred_format.name}' from file extension, "
                f"but format='{provided_format.name}' was specified."
            )
    return format


def save(
    data: pd.DataFrame,
    *,
    filepath: PathType,
    format: str | None = None,
    **kwargs,
) -> None:
    """Save a pandas DataFrame to a file, inferring the format from the file extension.

    Args:
        data: The DataFrame to save.
        filepath: Path to the output file.
        format: Explicit file format (optional). If provided, must match the file extension.
        **kwargs: Additional arguments passed to the underlying pandas IO method.
    """
    fmt = _resolve_format(filepath=filepath, input_format=format)
    save_method = fmt.save_method
    save_method(data=data, filepath=filepath, **kwargs)


def load(
    filepath: PathType,
    *,
    format: str | None = None,
    columns: list[str] | None = None,
    **kwargs,
) -> pd.DataFrame:
    """Load a pandas DataFrame from a file, optionally inferring the format from the file extension.

    Args:
        filepath: Path to the input file.
        format: Explicit file format (optional). If provided, must match the file extension.
        columns: The columns to load. If not specified, all columns are loaded.
        **kwargs: Additional arguments passed to the underlying pandas IO method.

    Returns:
        The loaded DataFrame.
    """

    fmt = _resolve_format(filepath=filepath, input_format=format, allow_conflict=True)
    load_method = fmt.load_method
    if fmt.name == CSV:
        if columns is not None:
            if "usecols" in kwargs:
                raise ValueError("Cannot specify both `columns` and `usecols`.")
            kwargs["usecols"] = columns
        return load_method(filepath=filepath, **kwargs)
    return load_method(filepath=filepath, columns=columns, **kwargs)
