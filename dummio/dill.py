"""IO for dill."""

from typing import Any

import dill
from upath import UPath

from dummio.constants import PathType


def save(data: Any, *, filepath: PathType) -> None:
    """Save a pickle file."""
    path = UPath(filepath)
    with path.open("wb") as file:
        dill.dump(data, file)


def load(filepath: PathType) -> Any:
    """Read a pickle file."""
    path = UPath(filepath)
    with path.open("rb") as file:
        return dill.load(file)
