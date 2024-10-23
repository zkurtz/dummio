"""Constants for ezio."""

from pathlib import Path
from typing import Any


type PathType = str | Path
type AnyDict = dict[Any, Any]

DEFAULT_ENCODING = "utf-8"
DEFAULT_WRITE_MODE = "w"