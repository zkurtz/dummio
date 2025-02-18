from pathlib import Path

import numpy as np

from dummio.numpy.ndarray_io import load, save


def test_ndarray_io(tmp_path: Path) -> None:
    # try a 3-d array and a filepath without extension:
    array = np.array([[[1, 2, 3], [4, 5, 6]]])
    filepath = tmp_path / "data"
    save(array, filepath=filepath)
    loaded_array = load(filepath)
    np.testing.assert_array_equal(array, loaded_array)

    array = np.array([1, 2, 3])
    filepath = tmp_path / "data.npy"
    save(array, filepath=filepath)
    loaded_array = load(filepath)
    np.testing.assert_array_equal(array, loaded_array)
