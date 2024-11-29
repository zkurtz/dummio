"""Constants for dummio."""

from pathlib import Path
from typing import Any, TypeAlias

PathType: TypeAlias = str | Path
AnyDict: TypeAlias = dict[Any, Any]

DEFAULT_ENCODING = "utf-8"
DEFAULT_WRITE_MODE = "w"
