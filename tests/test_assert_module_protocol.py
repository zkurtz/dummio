"""Assert that every IO module implements the ModuleProtocol."""

import importlib

from dummio import ModuleProtocol

IO_MODULES = [
    "dummio.json",
    "dummio.onnx",
    "dummio.text",
    "dummio.yaml",
    "dummio.pandas.df_csv",
    "dummio.pandas.df_parquet",
]


def test_assert_module_protocol() -> None:
    for module_name in IO_MODULES:
        module = importlib.import_module(module_name)
        assert isinstance(module, ModuleProtocol)
