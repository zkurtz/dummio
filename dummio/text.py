"""IO for text."""

from typing import Literal

from upath import UPath

from dummio.constants import DEFAULT_ENCODING, DEFAULT_WRITE_MODE, PathType


def save(
    data: str,
    *,
    filepath: PathType,
    encoding: str = DEFAULT_ENCODING,
    mode: Literal["r", "w", "a"] = DEFAULT_WRITE_MODE,
) -> None:
    """Save text."""
    path = UPath(filepath)
    with path.open(mode=mode, encoding=encoding) as file:
        file.write(data)


def load(filepath: PathType, encoding: str = DEFAULT_ENCODING) -> str:
    """Read text."""
    path = UPath(filepath)
    return path.read_text(encoding=encoding)
