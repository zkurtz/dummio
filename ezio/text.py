"""IO for text."""

from ezio.constants import AnyDict, PathType, DEFAULT_WRITE_MODE, DEFAULT_ENCODING


def save(data: str, *, filepath: PathType, encoding: str = DEFAULT_ENCODING, mode: str = DEFAULT_WRITE_MODE,) -> None:
    """Save text."""
    with open(filepath, mode, encoding=encoding) as file:
        file.write(data)


def load(filepath: PathType, encoding: str = DEFAULT_ENCODING) -> str:
    """Read text."""
    with open(filepath, "r", encoding=encoding) as file:
        return file.read()
