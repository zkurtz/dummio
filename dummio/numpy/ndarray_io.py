"""IO for numpy arrays.

These methods are thin wrappers over numpy.save and numpy.load. Main differences:
- These accept only str/path/upath-type filepath args (not a file-object)
- The provided filepath is the one that gets used, overriding default numpy.save behavior which appends a .npy extension
    to the filename if it does not already have one.
"""

from typing import Any

import numpy as np
from upath import UPath

from dummio.constants import PathType


def save(
    data: np.ndarray,
    *,
    filepath: PathType,
    **kwargs: Any,
) -> None:
    """Save numpy array to a npy file.

    Args:
        data: Numpy array to save.
        filepath: Path to save the data.
        **kwargs: Additional keyword arguments for numpy.save
    """
    path = UPath(filepath)
    with path.open("wb") as file:
        np.save(file=file, arr=data, **kwargs)


def load(filepath: PathType, **kwargs: Any) -> np.ndarray:
    """Read a npy file as a 1-d numpy array.

    Args:
        filepath: Path to read the data.
        **kwargs: Additional keyword arguments for numpy.load
    """
    path = UPath(filepath)
    with path.open("rb") as file:
        return np.load(file=file, **kwargs)


def example(filepath: PathType) -> None:
    """Example of using the numpy ndarray IO."""

    array = np.array([[[1, 2, 3], [4, 5, 6]]])
    print(f"Saving array to {filepath}")
    save(array, filepath=filepath)
    print(f"Loading array from {filepath}")
    loaded_array = load(filepath)
    np.testing.assert_array_equal(array, loaded_array)
