from pathlib import Path

import pandas as pd

from dummio.pandas import df_vortex


def test_io(tmp_path: Path) -> None:
    """Test basic vortex IO operations."""
    path = tmp_path / "data.vortex"
    data = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    df_vortex.save(data, filepath=path)
    loaded_data = df_vortex.load(path)
    pd.testing.assert_frame_equal(data, loaded_data)


def test_various_dtypes(tmp_path: Path) -> None:
    """Test vortex IO with various data types."""
    path = tmp_path / "data_types.vortex"
    data = pd.DataFrame(
        {
            "int_col": [1, 2, 3],
            "float_col": [1.1, 2.2, 3.3],
            "str_col": ["a", "b", "c"],
            "bool_col": [True, False, True],
        }
    )
    df_vortex.save(data, filepath=path)
    loaded_data = df_vortex.load(path)
    pd.testing.assert_frame_equal(data, loaded_data)


def test_with_nulls(tmp_path: Path) -> None:
    """Test vortex IO with null values."""
    path = tmp_path / "data_nulls.vortex"
    data = pd.DataFrame(
        {
            "a": [1, None, 3],
            "b": [None, 2.2, 3.3],
            "c": ["x", None, "z"],
        }
    )
    df_vortex.save(data, filepath=path)
    loaded_data = df_vortex.load(path)
    pd.testing.assert_frame_equal(data, loaded_data)
