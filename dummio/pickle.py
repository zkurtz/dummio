"""IO for pickle."""

import pickle
from typing import Any

from upath import UPath

from dummio.constants import PathType


def save(data: Any, *, filepath: PathType) -> None:
    """Save a pickle file."""
    path = UPath(filepath)
    with path.open("wb") as file:
        pickle.dump(data, file)


def load(filepath: PathType) -> Any:
    """Read a pickle file."""
    path = UPath(filepath)
    with path.open("rb") as file:
        return pickle.load(file)
