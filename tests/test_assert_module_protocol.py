"""Assert that every IO module implements save and load in a consistent way."""

import importlib

import pytest

from dummio.protocol import assert_module_protocol

IO_MODULES = [
    "dummio.json",
    "dummio.onnx",
    "dummio.pydantic",
    "dummio.text",
    "dummio.yaml",
    "dummio.pandas.df_csv",
    "dummio.pandas.df_parquet",
]


# decorate the test function with pytest.mark.parametrize
@pytest.mark.parametrize("module_path", IO_MODULES)
def test_assert_module_protocol(module_path: str) -> None:
    module = importlib.import_module(module_path)
    assert_module_protocol(module)
