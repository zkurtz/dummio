"""Constants for dummio."""

import typing
from pathlib import Path
from typing import Any, Protocol, TypeAlias

PathType: TypeAlias = str | Path
AnyDict: TypeAlias = dict[Any, Any]

# pyright expect a type var to be used at least twice within a single method. It's having
# trouble respecting how it's use *accross* methods of a class.
T = typing.TypeVar("T")  # pyright: ignore

DEFAULT_ENCODING = "utf-8"
DEFAULT_WRITE_MODE = "w"


@typing.runtime_checkable
class ModuleProtocol(Protocol):
    """Protocol for dummio's IO modules."""

    def save(self, data: T, *, filepath: PathType) -> None:  # pyright: ignore[reportInvalidTypeVarUse]
        """Declares the signature of an IO module save method."""
        ...

    def load(self, filepath: PathType) -> T:  # pyright: ignore[reportInvalidTypeVarUse]
        """Declares the signature of an IO module load method."""
        ...
