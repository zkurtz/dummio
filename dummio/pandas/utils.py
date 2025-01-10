"""Utilities for pandas IO."""

from typing import Any

from upath import UPath

from dummio.constants import PathType

STORAGE_OPTIONS = "storage_options"


def add_storage_options(*, filepath: PathType, kwargs: dict[str, Any]) -> None:
    """If filepath is a universal path, make sure that kwargs includes storage options.

    It's unclear exactly what are the circumstances where this is necessary. Follow the discussion at
    https://github.com/pandas-dev/pandas/issues/60618#issuecomment-2583469157.
    """
    if isinstance(filepath, UPath):
        if STORAGE_OPTIONS not in kwargs:
            kwargs[STORAGE_OPTIONS] = dict(filepath.storage_options)
