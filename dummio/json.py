"""IO for json."""

import json

from dummio.constants import DEFAULT_ENCODING, DEFAULT_WRITE_MODE, AnyDict, PathType


def save(
    data: AnyDict,
    *,
    filepath: PathType,
    encoding: str = DEFAULT_ENCODING,
    mode: str = DEFAULT_WRITE_MODE,
) -> None:
    """Save a json file."""
    with open(filepath, mode, encoding=encoding) as file:
        json.dump(data, file)


def load(filepath: PathType, encoding: str = DEFAULT_ENCODING) -> AnyDict:
    """Read a json file."""
    with open(filepath, "r", encoding=encoding) as file:
        return json.load(file)
