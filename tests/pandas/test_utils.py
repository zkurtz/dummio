from pathlib import Path

from upath import UPath

from dummio.pandas.utils import STORAGE_OPTIONS, add_storage_options


def test_add_storage_options() -> None:
    """Test the add_storage_options function."""
    kwargs = {}
    path = UPath("s3://bucket/data.parquet")
    add_storage_options(filepath=path, kwargs=kwargs)
    assert STORAGE_OPTIONS in kwargs

    kwargs = {}
    path = UPath("data.parquet")
    add_storage_options(filepath=path, kwargs=kwargs)
    assert STORAGE_OPTIONS in kwargs

    kwargs = {}
    add_storage_options(filepath=Path("data.parquet"), kwargs=kwargs)
    assert STORAGE_OPTIONS not in kwargs
