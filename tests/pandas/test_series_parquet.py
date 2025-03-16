from pathlib import Path

import pandas as pd

from dummio import pandas as pd_io


def build_series() -> pd.Series:
    """Create a series in a format that parquet would preserve but json would not."""
    idx = pd.CategoricalIndex(["a", "b", "c"], categories=["a", "b", "c", "d"])
    return pd.Series([1, None, 3], index=idx, dtype="Int64")


def test_io(tmp_path: Path) -> None:
    path = tmp_path / "data"
    data = build_series()
    pd_io.series_parquet.save(data, filepath=path)
    loaded_data = pd_io.series_parquet.load(path)
    pd.testing.assert_series_equal(data, loaded_data)

    # try a named series:
    data.name = "hello"
    pd_io.series_parquet.save(data, filepath=path)
    loaded_data = pd_io.series_parquet.load(path)
    pd.testing.assert_series_equal(data, loaded_data)

    # another unnamed series:
    series = pd.Series([1, 2, 3])
    pd_io.series_parquet.save(series, filepath=path)
