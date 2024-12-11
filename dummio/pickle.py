"""IO for pickle."""

import pickle
from typing import Any

from dummio.constants import PathType


def save(data: Any, *, filepath: PathType) -> None:
    """Save a pickle file."""
    with open(filepath, "wb") as file:
        pickle.dump(data, file)


def load(filepath: PathType) -> Any:
    """Read a pickle file."""
    with open(filepath, "rb") as file:
        return pickle.load(file)
