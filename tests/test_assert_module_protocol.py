"""Assert that every IO module implements save and load in a consistent way."""

import importlib
from typing import Callable, get_type_hints

from dummio.constants import PathType

IO_MODULES = [
    "dummio.json",
    "dummio.onnx",
    "dummio.pydantic",
    "dummio.text",
    "dummio.yaml",
    "dummio.pandas.df_csv",
    "dummio.pandas.df_parquet",
]


def test_assert_module_protocol() -> None:
    for module_name in IO_MODULES:
        module = importlib.import_module(module_name)
        assert hasattr(module, "save")
        assert hasattr(module, "load")

        # make the following assertions about the save attribute:
        # - it is a function
        # - the first argument is named "data"
        # - all subsequent arguments are keyword-only
        # - the second argument is "filepath" of type dummio.constants.PathType
        assert isinstance(module.save, Callable)
        signature = get_type_hints(module.save)
        first_two_args = list(signature.keys())[:2]
        assert first_two_args == ["data", "filepath"]
        assert signature["filepath"] == PathType

        # make the following assertions about the load attribute:
        # - it is a function
        # - the first argument is named "filepath", of type dummio.constants.PathType
        # - the return type is the same as the "data" argument of the save function
        assert isinstance(module.load, Callable)
        signature = get_type_hints(module.load)
        first_arg = list(signature.keys())[0]
        assert first_arg == "filepath"
        assert signature["filepath"] == PathType
        assert signature["return"] == get_type_hints(module.save)["data"]
