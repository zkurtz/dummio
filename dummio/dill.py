"""IO for dill."""

from typing import Any

import dill

from dummio.constants import PathType


def save(data: Any, *, filepath: PathType) -> None:
    """Save a dill file."""
    with open(filepath, "wb") as file:
        dill.dump(data, file)


def load(filepath: PathType) -> Any:
    """Read a dill file."""
    with open(filepath, "rb") as file:
        return dill.load(file)
