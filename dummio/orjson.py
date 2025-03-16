"""IO for json using orjson."""

import orjson
from upath import UPath

from dummio.constants import AnyDict, PathType


def save(
    data: AnyDict,
    *,
    filepath: PathType,
    option: int | None = None,
) -> None:
    """Save a json file using orjson.

    Args:
        data: Data to save.
        filepath: Path to save the data.
        encoding: Encoding to use.
        mode: Write mode.
        option: orjson options flag, e.g., orjson.OPT_INDENT_2, orjson.OPT_SERIALIZE_NUMPY
    """
    data_bytes = orjson.dumps(data, option=option)
    if isinstance(filepath, UPath):
        filepath.write_bytes(data_bytes)
    else:
        with open(filepath, "wb") as file:  # Binary mode for orjson
            file.write(data_bytes)


def load(filepath: PathType) -> AnyDict:
    """Read a json file using orjson."""
    if isinstance(filepath, UPath):
        data_bytes = filepath.read_bytes()
        return orjson.loads(data_bytes)
    else:
        with open(filepath, "rb") as file:  # Binary mode for orjson
            return orjson.loads(file.read())
