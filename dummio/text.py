"""IO for text."""

from upath import UPath

from dummio.constants import DEFAULT_ENCODING, PathType


def save(
    data: str,
    *,
    filepath: PathType,
    encoding: str = DEFAULT_ENCODING,
) -> None:
    """Save text."""
    path = UPath(filepath)
    path.write_text(data, encoding=encoding)


def load(filepath: PathType, encoding: str = DEFAULT_ENCODING) -> str:
    """Read text."""
    path = UPath(filepath)
    return path.read_text(encoding=encoding)
