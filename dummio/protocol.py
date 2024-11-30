"""Runtime validation of the dummio module protocol."""

from types import ModuleType
from typing import Callable, get_type_hints

from dummio.constants import PathType


def assert_module_protocol(module: ModuleType) -> None:
    """Assert that a module implements save and load in a consistent way."""
    if not hasattr(module, "save"):
        raise AttributeError("Module is missing 'save' attribute")
    if not hasattr(module, "load"):
        raise AttributeError("Module is missing 'load' attribute")

    # make the following assertions about the save attribute:
    # - it is a function
    # - the first argument is named "data"
    # - all subsequent arguments are keyword-only
    # - the second argument is "filepath" of type dummio.constants.PathType
    if not isinstance(module.save, Callable):
        raise TypeError("'save' attribute is not callable")
    signature = get_type_hints(module.save)
    first_two_args = list(signature.keys())[:2]
    if first_two_args != ["data", "filepath"]:
        raise TypeError("First two arguments of 'save' must be 'data' and 'filepath'")
    if signature["filepath"] != PathType:
        raise TypeError("'filepath' argument of 'save' must be of type PathType")

    # make the following assertions about the load attribute:
    # - it is a function
    # - the first argument is named "filepath", of type dummio.constants.PathType
    # - the return type is the same as the "data" argument of the save function
    if not isinstance(module.load, Callable):
        raise TypeError("'load' attribute is not callable")
    signature = get_type_hints(module.load)
    first_arg = list(signature.keys())[0]
    if first_arg != "filepath":
        raise TypeError("First argument of 'load' must be 'filepath'")
    if signature["filepath"] != PathType:
        raise TypeError("'filepath' argument of 'load' must be of type PathType")
    if signature["return"] != get_type_hints(module.save)["data"]:
        raise TypeError("Return type of 'load' must match 'data' argument type of 'save'")
