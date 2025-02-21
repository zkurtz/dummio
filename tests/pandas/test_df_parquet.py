from pathlib import Path

import pandas as pd
import pytest

from dummio.pandas import df_parquet


def test_io(tmp_path: Path) -> None:
    """Test the packio package for IO for tabular data."""
    path = tmp_path / "data"
    data = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    df_parquet.save(data, filepath=path)
    loaded_data = df_parquet.load(path)
    pd.testing.assert_frame_equal(data, loaded_data)

    # suppose one column is unnamed
    data = pd.DataFrame({None: [1, 2], "b": [3, 4]})
    df_parquet.save(data, filepath=path)
    loaded_data = df_parquet.load(path)
    pd.testing.assert_frame_equal(data, loaded_data)

    # expect a useful error message if using fastparquet with a column named None
    with pytest.raises(ValueError, match=r"specify engine='pyarrow', not 'fastparquet'.*support None column names."):
        df_parquet.save(data, filepath=path, engine="fastparquet")
    # but should work fine with pyarrow
    df_parquet.save(data, filepath=path, engine="pyarrow")
