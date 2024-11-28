from pathlib import Path
from types import ModuleType

import pandas as pd

from dummio import pandas as pd_io


def dataframe() -> pd.DataFrame:
    return pd.DataFrame({"a": [1, 2], "b": [3, 4]})


def _assert_cycle(*, data: pd.DataFrame, path: Path, module: ModuleType) -> None:
    """Apply the module save/load cycle on the data and assert that the reloaded data matches the input data."""
    module.save(data, filepath=path)
    loaded_data = module.load(path)
    pd.testing.assert_frame_equal(data, loaded_data)


def test_df_io(tmp_path: Path) -> None:
    """Test the packio package for IO for tabular data."""
    modules = [
        pd_io.df_parquet,
        pd_io.df_csv,
    ]
    for module in modules:
        _assert_cycle(
            data=dataframe(),
            path=tmp_path / "data",
            module=module,
        )
