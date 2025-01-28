"""IO for json."""

import json

from upath import UPath

from dummio.constants import DEFAULT_ENCODING, DEFAULT_WRITE_MODE, AnyDict, PathType


def save(
    data: AnyDict,
    *,
    filepath: PathType,
    encoding: str = DEFAULT_ENCODING,
    mode: str = DEFAULT_WRITE_MODE,
    indent: int = 4,
) -> None:
    """Save a json file.

    Args:
        data: Data to save.
        filepath: Path to save the data.
        encoding: Encoding to use.
        mode: Write mode.
        indent: Number of spaces of indentation for the json file.
    """
    if isinstance(filepath, UPath):
        data_str = json.dumps(data, indent=indent)
        filepath.write_text(data_str, encoding=encoding)
    else:
        with open(filepath, mode, encoding=encoding) as file:
            json.dump(data, file)


def load(filepath: PathType, encoding: str = DEFAULT_ENCODING) -> AnyDict:
    """Read a json file."""
    if isinstance(filepath, UPath):
        data_str = filepath.read_text(encoding=encoding)
        return json.loads(data_str)
    with open(filepath, "r", encoding=encoding) as file:
        return json.load(file)
