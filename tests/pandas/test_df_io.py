import shutil
from pathlib import Path

import pandas as pd
import pytest

from dummio.pandas.df_io import load, save


def test_df_io(tmp_path: Path) -> None:
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    save(df, filepath=tmp_path / "data.csv")
    save(df, filepath=tmp_path / "data.csv", format="csv")
    pd.testing.assert_frame_equal(df, load(tmp_path / "data.csv"))
    pd.testing.assert_frame_equal(df, load(tmp_path / "data.csv", format="csv"))

    # Do not permit the creation of a file with a misleading extension:
    msg = "Conflicting format information: inferred 'csv' from file extension, " "but format='parquet' was specified"
    with pytest.raises(ValueError, match=msg):
        save(df, filepath=tmp_path / "data.csv", format="parquet")

    # However, it's fine to try loading a misnamed file by correcting the format:
    shutil.move(tmp_path / "data.csv", tmp_path / "data.feather")
    pd.testing.assert_frame_equal(df, load(tmp_path / "data.feather", format="csv"))

    # Also it's permitted to skip the extension when writing a file:
    save(df, filepath=tmp_path / "data", format="feather")
    pd.testing.assert_frame_equal(df, load(tmp_path / "data", format="feather"))
